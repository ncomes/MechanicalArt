# ! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates IK Spline rig to be used on Leaper tongue.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.common.utils import lists
from mca.mya.utils import naming
from mca.mya.modifiers import ma_decorators
# Internal module imports
from mca.mya.rigging.tek import tek_base, spline_ik_component


class LeaperTongueComponent(spline_ik_component.SplineIKComponent):
    VERSION = 1

    ATTACH_ATTRS = ['retract', 'spore', 'spore_scale']

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(tek_parent,
               start_joint,
               end_joint,
               end_helper_joint,
               mid_helper_joint,
               side,
               region,
               start_helper_joint=None,
               mid_flag=True,
               can_retract=True,
               **kwargs):
        """
        This wraps the complex spline IK component and adds the projectile feature.

        :param TEKNode tek_parent: TEK Rig TEKNode.
        :param Joint start_joint: Start joint of the chain.
        :param Joint end_joint: End joint of the chain.
        :param Joint start_helper_joint: A joint separated, but co-located with the start joint of the primary chain. If a joint is not supplied a flag will not be created for this.
        :param Joint end_helper_joint: A joint separated, but co-located with the end joint of the primary chain
        :param Joint mid_helper_joint: A joint located between the start/end joint, but not part of the primary chain
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :param bool mid_flag: If we should create a mid component flag.
        :param bool can_retract: If this component will be setup with the ability to retract.
        :return: The newly created SplineIKComponent
        :rtype: SplineIKComponent
        """

        root_namespace = tek_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = spline_ik_component.SplineIKComponent.create(tek_parent,
                                                            start_joint,
                                                            end_joint,
                                                            end_helper_joint,
                                                            mid_helper_joint,
                                                            side,
                                                            region,
                                                            start_helper_joint=start_helper_joint,
                                                            mid_flag=True,
                                                            can_retract=True,
                                                            **kwargs)

        # reset our node types.
        node.setAttr(tek_base.TEK_TYPE_ATTR, LeaperTongueComponent.__name__)
        node.setAttr('version', LeaperTongueComponent.VERSION)

        # get the objects we need to set the scale
        end_flag = node.end_flag.get()
        helper_joint = node.helper_joint.get()
        leaf_joint_list = node.leafJoints.get()[1:-1]

        # add attrs and connection them so we can recover them later.
        for x in [end_flag, helper_joint]:
            if not x.hasAttr('spore'):
                x.addAttr('spore', dv=0, min=0, max=10, k=True)
            if not x.hasAttr('spore_scale'):
                x.addAttr('spore_scale', dv=1, min=.6, max=10, k=True)
        end_flag.spore >> helper_joint.spore
        end_flag.spore_scale >> helper_joint.spore_scale

        increment_value = 10 / (len(leaf_joint_list)+1)
        # add our total scale modifiers in
        max_scale = pm.createNode('plusMinusAverage', n=f'{region}_{side}_spore_max_scale')
        max_scale.input1D[0].set(-1)
        end_flag.spore_scale >> max_scale.input1D[1]
        max_scale.operation.set(2)
        mult_nodes = []
        remap_nodes = []
        add_nodes = []

        add_nodes.append(max_scale)

        for index, leaf_joint_node in enumerate(leaf_joint_list):
            # we want a min scale of 1 so the ends of our bell curve are equal to 1
            # we want a max of 2 scale so our sum at our peek is 2
            # equation looks like this -N*X^2 + -2N*X + 1
            # N is our max scale output, X is our remap out
            # this creates a parabola in the 0-2 range with 1 at it's peek
            remap = pm.createNode('remapValue', n=f'{naming.get_basename(leaf_joint_node)}_remap')
            remap_nodes.append(remap)
            end_flag.spore >> remap.inputValue
            remap.inputMin.set(index * increment_value)
            remap.inputMax.set((index + 2) * increment_value)
            remap.outputMin.set(0)
            remap.outputMax.set(2)

            # this handles the X^2 and -2X portion of our equation
            input_multi = pm.createNode('multiplyDivide', n=f'{naming.get_basename(leaf_joint_node)}_input_multi')
            mult_nodes.append(input_multi)
            remap.outValue >> input_multi.input1X
            remap.outValue >> input_multi.input2X
            input_multi.input1Y.set(-2)
            max_scale.output1D >> input_multi.input2Y

            # this handles the -N and N portion of our equation
            parabola_multi = pm.createNode('multiplyDivide', n=f'{naming.get_basename(leaf_joint_node)}_parabola_multi')
            mult_nodes.append(parabola_multi)
            max_scale.output1D >> parabola_multi.input1X
            input_multi.outputX >> parabola_multi.input2X

            input_multi.outputY >> parabola_multi.input1Y
            remap.outValue >> parabola_multi.input2Y

            # add it all together to get our finished quadratic
            scale_sum = pm.createNode('plusMinusAverage', n=f'{naming.get_basename(leaf_joint_node)}_scale_sum')
            add_nodes.append(scale_sum)
            parabola_multi.outputX >> scale_sum.input1D[0]
            parabola_multi.outputY >> scale_sum.input1D[1]
            scale_sum.input1D[2].set(1)

            # apply it to our live joints.
            original_plug = lists.get_first_in_list(leaf_joint_node.sz.listConnections(p=True))
            if not original_plug:
                # if the original component could not retract.
                scale_sum.output1D >> leaf_joint_node.sy
                scale_sum.output1D >> leaf_joint_node.sz
            else:
                # if the base component could retract we'll want to disconnect that and merge our scale values.
                pm.disconnectAttr(leaf_joint_node.sy)
                pm.disconnectAttr(leaf_joint_node.sz)

                retract_merge_multi = pm.createNode('multiplyDivide', n=f'{naming.get_basename(leaf_joint_node)}_retract_merge_multi')
                mult_nodes.append(retract_merge_multi)

                original_plug >> retract_merge_multi.input1X
                scale_sum.output1D >> retract_merge_multi.input2X

                retract_merge_multi.outputX >> leaf_joint_node.sy
                retract_merge_multi.outputX >> leaf_joint_node.sz

        node.connect_nodes(remap_nodes, 'remapNodes', 'tekParent')
        node.connect_nodes(mult_nodes, 'multNodes', 'tekParent')
        node.connect_nodes(add_nodes, 'addNodes', 'tekParent')

        return node

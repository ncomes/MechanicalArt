#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to base FRAGNodes and their usage.
"""

# python imports
import abc
import collections
import os

# software specific imports
import maya.cmds as cmds
import pymel.all as pm

# Project python imports
from mca.common.assetlist import assetlist
from mca.common.utils import list_utils, fileio, pymaths, string_utils
from mca.common.textio import yamlio

from mca.mya.animation import baking, time_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.utils import attr_utils, constraint_utils, dag_utils, naming, namespace_utils
from mca.mya.utils.om import om_utils

from mca.mya.rigging import flags, joint_utils
from mca.mya.rigging.frag import frag_base
from mca.mya.rigging.frag.components import frag_root

from mca.common import log
logger = log.MCA_LOGGER

class FRAGRig(frag_root.FRAGRootSingle):
    _version = 1.0

    @classmethod
    def create(cls, frag_parent, **kwargs):
        new_frag_node = super().create(frag_parent=frag_parent, **kwargs)
        frag_root_node = new_frag_node.get_frag_root()

        new_frag_node.pynode.addAttr('rig_scale', at='float')
        frag_root_node.add_asset_group().sx >> new_frag_node.pynode.rig_scale
        
        return new_frag_node

    def _remove(self):
        for frag_component in self.get_frag_children():
            if isinstance(frag_component, FRAGAnimatedComponent):
                for flag_node in frag_component.flags:
                    flag_pynode = flag_node.pynode
                    if flag_pynode.hasAttr('source_multi_constraint'):
                        multiconstraint_node = flag_pynode.getAttr('source_multi_constraint')
                        if multiconstraint_node:
                            multiconstraint_node = frag_base.FRAGNode(multiconstraint_node)
                        if multiconstraint_node:
                            multiconstraint_node.remove()
            try:
                frag_component.remove()
            except:
                pass
        rig_group = self.rig_group
        if rig_group:
            pm.delete(rig_group)
        try:
            pm.delete(self.pynode)
        except:
            pass

    def remove(self):
        self.frag_parent.remove()

    @property
    def rig_version(self):
        if self.pynode.hasAttr('rig_version'):
            return self.pynode.getAttr('rig_version')
        return 1.0

    @rig_version.setter
    def rig_version(self, val):
        if not self.pynode.hasAttr('rig_version'):
            self.pynode.addAttr('rig_version', at='float')
        self.pynode.setAttr('rig_version', val)

    @property
    def rig_file(self):
        if self.pynode.hasAttr('rig_file'):
            return self.pynode.getAttr('rig_file')

    @rig_file.setter
    def rig_file(self, val):
        if not self.pynode.hasAttr('rig_file'):
            self.pynode.addAttr('rig_file', dt='string')
        self.pynode.setAttr('rig_file', val)

    @property
    def rig_scale(self):
        # NOTE: the rig scale is based on the asset_group's scale
        rig_scale = 1.0
        if self.pynode.hasAttr('rig_scale'):
            rig_scale = self.pynode.getAttr('rig_scale')
        return rig_scale
    
    @property
    def rig_group(self):
        if self.pynode.hasAttr('rig_group'):
            return self.pynode.getAttr('rig_group')

    @rig_group.setter
    def rig_group(self, rig_group):
        self.connect_node(rig_group, 'rig_group', 'frag_parent')

    def add_rig_group(self):
        rig_group = self.rig_group
        if not self.rig_group:
            rig_group = self._create_managed_group('rig_group')
            rig_group.setParent(self.frag_parent.add_asset_group())

            self.rig_group = rig_group
        return rig_group

    @property
    def do_not_touch_group(self):
        if self.pynode.hasAttr('do_not_touch_group'):
            return self.pynode.getAttr('do_not_touch_group')

    @do_not_touch_group.setter
    def do_not_touch_group(self, do_not_touch_group):
        self.connect_node(do_not_touch_group, 'do_not_touch_group', 'frag_parent')

    def add_do_not_touch_group(self):
        do_not_touch_group = self.do_not_touch_group
        if not self.do_not_touch_group:
            do_not_touch_group = self._create_managed_group('DO_NOT_TOUCH')
            do_not_touch_group.setParent(self.add_rig_group())

            self.do_not_touch_group = do_not_touch_group
        return do_not_touch_group

    @property
    def flags_group(self):
        if self.pynode.hasAttr('flags_group'):
            return self.pynode.getAttr('flags_group')

    @flags_group.setter
    def flags_group(self, flags_group):
        self.connect_node(flags_group, 'flags_group', 'frag_parent')

    def add_flags_group(self):
        flags_group = self.flags_group
        if not self.flags_group:
            flags_group = self._create_managed_group('flags_all')
            flags_group.setParent(self.add_rig_group())

            self.flags_group = flags_group
        if flags_group:
            frag_display_node = self.get_frag_root().frag_display
            if frag_display_node:
                asset_name = self.get_frag_root().asset_name
                display_layer_name = f'{asset_name}_flags_dl'
                frag_display_node.add_display_layer(display_layer_name)
                frag_display_node.add_objects_to_layer(display_layer_name, flags_group)
        return flags_group

    def get_all_flags(self):
        """
        Get all flags on all components.

        :return: A list of wrapped flag nodes.
        :rtype: Flag
        """
        return_list = []
        animated_component_list = self.get_frag_children(frag_type=FRAGAnimatedComponent)
        for animated_component in animated_component_list:
            return_list += animated_component.flags
        return return_list
    
    def zero_flags(self):
        """
        Set all flag transform values back to 0 (or 1.0 for scale) any custom attrs will be set back to their default values.

        """
        for wrapped_flag in self.get_all_flags():
            flag_pynode = wrapped_flag.pynode
            for attr in flag_pynode.listAttr(keyable=True):
                if attr.isLocked() or attr.isHidden():
                    continue
                else:
                    if attr.shortName() in attr_utils.TRANSLATION_ATTRS+attr_utils.ROTATION_ATTRS:
                        attr.set(0.0)
                    elif attr.shortName() in attr_utils.SCALE_ATTRS:
                        attr.set(1.0)
                    elif attr.isDynamic():
                        if 'follow' in attr.name():
                            continue
                        default_value = pm.addAttr(attr, q=1, dv=1)
                        try:
                            attr.set(default_value)
                        except:
                            continue

    def _sort_flags(self, color=True, flags_path=None):
        frag_display_node = self.get_frag_root().frag_display
        flag_list = self.get_all_flags()

        contact_flag_list = []
        detail_flag_list = []
        for wrapped_flag in flag_list:
            if flags_path:
                wrapped_flag.swap_shape(flag_path=os.path.join(flags_path, naming.get_basename(wrapped_flag.pynode)))
            # Color after swapping flags.
            if color:
                self._color_flag(wrapped_flag)
            
            # No need to sort flags if we don't have a FRAGDisplay node.
            if not frag_display_node:
                logger.debug('FRAGDisplay was missing from this FRAGRoot')
                continue
            if wrapped_flag.detail:
                detail_flag_list.append(wrapped_flag.pynode)
            elif wrapped_flag.contact:
                contact_flag_list.append(wrapped_flag.pynode)

        asset_name = self.get_frag_root().asset_name
        if contact_flag_list:
            display_layer_name = f'{asset_name}_contact_flags_dl'
            frag_display_node.add_display_layer(display_layer_name)
            frag_display_node.add_objects_to_layer(display_layer_name, contact_flag_list)
        if detail_flag_list:
            display_layer_name = f'{asset_name}_detail_flags_dl'
            frag_display_node.add_display_layer(display_layer_name)
            frag_display_node.add_objects_to_layer(display_layer_name, detail_flag_list)
        return flag_list

    def _color_flag(self, flag):
        flag_pynode = flag.pynode
        flag_shape_list = flag_pynode.getShapes()
        # using the shape here gets around dispaly layer organization.
        for flag_shape in flag_shape_list:
            flag_shape.overrideEnabled.set(1)
            if flag.detail:
                flag_shape.overrideColor.set(9)
            elif flag.contact:
                flag_shape.overrideColor.set(14)
            elif flag.utility:
                flag_shape.overrideColor.set(19)
            elif flag.sub:
                flag_shape.overrideColor.set(18)
            else:
                flag_side = flag.side
                if flag_side == 'left':
                    flag_shape.overrideColor.set(6)
                elif flag_side == 'right':
                    flag_shape.overrideColor.set(13)
                elif flag_side == 'center':
                    flag_shape.overrideColor.set(17)
                elif flag_side == 'front':
                    flag_shape.overrideColor.set(20)
                elif flag_side == 'back':
                    flag_shape.overrideColor.set(19)

    def finish_rig(self, flags_path=None):
        """
        Swap flag shapes, color flags, and organize them into dispaly layers.

        :param str flags_path: Path to the directory we want to load flags from.
        """
        if not flags_path:
            asset_id = self.asset_id
            try:
                asset_entry = assetlist.get_asset_by_id(asset_id)
                if asset_entry:
                    flags_path = asset_entry.flags_path
            except:
                pass
        self._sort_flags(color=True, flags_path=flags_path)

    def validate_rig(self):
        """
        Check all child components to see if they're at the latest version. If they're not return false.

        :return: If the validatation was successful or not.
        :rtype: bool
        """
        for frag_component in self.get_frag_children():
            try:
                if frag_component.version != frag_base.FRAGNodeRegister._FRAGNODE_TYPES.get(frag_component.frag_type)._version:
                    return False
            except:
                logger.error(f'{frag_component.frag_Type}: A frag type was not found.')
                return False
        return True

    @ma_decorators.keep_namespace_decorator
    def reload(self, force=False, full=False):
        """
        Reload this rig if there is a discrepancy in component versions, or we force it to.

        :param bool force: If we should reload the rig even if it's up to date.
        :param bool full: If we're going to rebuild it from scratch.
        :return: The new or un modified FRAGRig
        :rtype: FRAGRig
        """
        frag_rig = self
        if force or not self.validate_rig():
            # If we're forcing or the validation is false.
            namespace_utils.set_namespace('')
            asset_id = self.asset_id
            asset_entry = assetlist.get_asset_by_id(asset_id)
            if not asset_entry:
                # We failed to find a lookup so we can't reload safely.
                logger.error(f'{asset_id}, {self.get_frag_root().asset_name}: Failed to find a lookup for this asset')
                return self
            rig_file = self.rig_file
            if not rig_file:
                # We failed to find the rig file associated with this rig and will be unable to reload it.
                logger.error(f'{asset_id}, {self.get_frag_root().asset_name}: Failed to find a registered rig file.')
                return self
            rig_path = os.path.join(asset_entry.rig_path, rig_file)
            if not os.path.exists(rig_path):
                logger.error(f'{rig_path}: Rig file was not found on disk.')
                return self
            
            if full:
                skel_path = asset_entry.skeleton_path
                if not skel_path or not os.path.exists(skel_path):
                    logger.error(f'{skel_path}: Skeleton file was not found on disk.')
                    return self

            # Step one, save our animation if we have any.
            logger.debug(f'Step one, animation Check')
            frame_range = time_utils.get_keyframe_range_from_nodes([x.pynode for x in self.get_all_flags()])
            bake_root = None
            if any(frame_range):
                bake_root = self.bake_rig_to_skeleton()

            # Step two, recover our build namespace.
            logger.debug(f'Step two, namespace check')
            rig_namespace = self.pynode.namespace()
            if rig_namespace:
                namespace_utils.set_namespace(rig_namespace)

            # Step three, remove the current rig.
            logger.debug(f'Step three, remove rig')
            if full:
                self.remove()
                root_joint = joint_utils.import_skeleton(skel_path)
                new_frag_root = frag_root.FRAGRoot.create(root_joint, asset_id)
                frag_rig = FRAGRig.create(new_frag_root)
            else:
                frag_root = self.get_frag_root()
                self._remove()
                frag_rig = FRAGRig.create(frag_root)
            
            # Step four, rebuild the current rig.
            logger.debug(f'Step four, load rig')
            load_serialized_rig(frag_rig, rig_path)

            # step five, (optional) restore animation.
            logger.debug(f'Step five, rebake anims')
            if bake_root:
                frag_rig.bake_skeleton_to_rig(bake_root)

        return frag_rig

    # Rig serialization functions.
    def serialize_rig(self, increment_version=False):
        """
        From a build rig, serialize all the rig data to dictionaries that contain the information required to rebuild them.

        :return: A list of dictionaries containing the information required to rebuild all rig components.
        :rtype: list[dict, ...]
        """
        frag_root = self.get_frag_root()
        root_joint = frag_root.root_joint
        skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        # Handle versioning.
        version = None
        if increment_version:
            version = int(self.rig_version + 1)
            self.rig_version = version
        rig_build_dict = {'components':[]}
        rig_build_dict['version'] = version or self.rig_version

        # Serialize all components.
        for frag_component in self.get_frag_children():
            frag_type = frag_component.frag_type
            if frag_type in ['TwistComponent', 'MultiConstraintComponent']:
                # Twist components are handled automatically independent of normal rig components, along wiht MultiConstraints.
                continue
            component_dict, skel_hierarchy = frag_component.serialize_component(skel_hierarchy)
            rig_build_dict['components'].append(component_dict)

        return rig_build_dict
    
    def attach_to_skeleton(self, skel_hierarchy):
        things_to_delete = []
        things_to_bake = []
        attrs_to_bake = []
        for frag_component in self.get_frag_children(frag_type=FRAGAnimatedComponent):
            skel_hierarchy, more_things_to_delete = frag_component.attach_to_skeleton(skel_hierarchy.root, skel_hierarchy)
            things_to_delete += more_things_to_delete
            bakeable_flags, component_attr_list, _ = frag_component.get_bakeable_rig_nodes()
            things_to_bake += bakeable_flags
            attrs_to_bake += component_attr_list
        return things_to_bake, attrs_to_bake, things_to_delete
    
    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    @ma_decorators.keep_selection_decorator
    @ma_decorators.not_undoable_decorator
    def bake_rig_to_skeleton(self, start_frame=None, end_frame=None, set_to_zero=True):
        # Disable autokey
        cmds.autoKeyframe(state=False)

        # Step one, check our frame range.
        if None in [start_frame, end_frame]:
            flag_pynode_list = [x.pynode for x in self.get_all_flags()]
            start_frame, end_frame = time_utils.get_times(flag_pynode_list)

        # Step two, get a fresh skeleton.
        asset_id = self.asset_id
        skeleton_path = assetlist.get_asset_by_id(asset_id).skeleton_path
        if skeleton_path and os.path.exists(skeleton_path):
            bake_root = joint_utils.import_merge_skeleton(skeleton_path, None)
        else:
            return

        # Step three, attach our fresh skel to our rig skel.
        rig_root = self.get_frag_root().root_joint
        custom_attrs = joint_utils.attach_skeletons(rig_root, bake_root)

        # Step four, bake!
        joint_list = [bake_root]+pm.listRelatives(bake_root, ad=True, type=pm.nt.Joint)
        if start_frame != end_frame:
            baking.bake_objects(joint_list, bake_range=[start_frame, end_frame], custom_attrs=custom_attrs)
        else:
            cmds.currentTime(start_frame)
            pm.setKeyframe(joint_list)
            pm.delete(pm.listRelatives(bake_root, ad=True, type=pm.nt.Constraint))

        # Step five, do we need to zero animations?
        if set_to_zero and start_frame != 0.0:
            keyframe_dif = 0.0 - start_frame
            om_utils.om2_change_curve_start_time(joint_list, keyframe_dif)
        pm.delete(pm.listRelatives(bake_root, ad=True, type=pm.nt.Constraint))
        return bake_root

    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    @ma_decorators.keep_selection_decorator
    @ma_decorators.keep_namespace_decorator
    @ma_decorators.not_undoable_decorator
    def bake_skeleton_to_rig(self, root_joint, start_frame=None, end_frame=None, append=False, motion_encode=True):
        """
        
        """
        # Disable autokey and set our namespace to something safe.
        namespace_utils.set_namespace('')
        cmds.autoKeyframe(state=False)

        # Step one get our skel frame range, and set our markup
        asset_id = self.asset_id
        skeleton_path = assetlist.get_asset_by_id(asset_id).skeleton_path
        if skeleton_path and os.path.exists(skeleton_path):
            joint_utils.reset_markup(skeleton_path, root_joint)
        else:
            logger.error(f'{skeleton_path}, Skeleton does not exist on disk, errors may occur when attaching.')
        skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)
        skel_start_frame, skel_end_frame = time_utils.get_keyframe_range_from_nodes(node_list=skel_hierarchy.animated_joints)

        # Step two, do we need to move our animation?
        current_end_frame = 0.0
        current_start_frame = 0.0
        if append:
            current_start_frame, current_end_frame = time_utils.get_keyframe_range_from_nodes([x.pynode for x in self.get_all_flags()])
            if None in [current_start_frame, current_end_frame]:
                current_start_frame = 0.0
                current_end_frame = 0.0

        keyframe_dif = 0.0
        if current_end_frame != skel_start_frame:
            keyframe_dif = current_end_frame - current_start_frame
        
        start_frame = start_frame or skel_start_frame
        end_frame = end_frame or skel_end_frame
        if keyframe_dif != 0.0:
            om_utils.om2_change_curve_start_time(skel_hierarchy.animated_joints, keyframe_dif)
            start_frame = current_end_frame
            end_frame = current_end_frame+abs(skel_start_frame)+abs(skel_end_frame)

        # Step three, do we need to offset our incomming animation?
        if motion_encode and append:
            if current_start_frame != current_end_frame:
                # If our start and ends are different we have animation, so lets get our alignment down.
                # We need to go to the end of our current animation and align our groups.
                cmds.currentTime(current_end_frame)
                motion_encode_grp = pm.group(n='motion_encode', w=True, em=True)
                pm.delete(pm.parentConstraint(skel_hierarchy.root, motion_encode_grp))
                skel_hierarchy.root.setParent(motion_encode_grp)
                rig_root = self.get_frag_root().root_joint
                pm.delete(pm.parentConstraint(rig_root, motion_encode_grp))

        # Step four, Alignment
        self.zero_flags()
        if skeleton_path and os.path.exists(skeleton_path):
            joint_utils.import_merge_skeleton(skeleton_path, skel_hierarchy.root)
        else:
            logger.error(f'{skeleton_path}, Skeleton does not exist on disk, errors may occur when attaching.')
        
        # Step five, Attach
        things_to_bake, attrs_to_bake, things_to_delete = self.attach_to_skeleton(skel_hierarchy)
        cmds.currentTime(cmds.currentTime(q=True))

        # Step sixe, bake
        attrs_to_bake = list(set(attrs_to_bake))
        # Trim out a few attrs we want to ignore.
        if 'ikTwist' in attrs_to_bake:
            # This gets baked down to the skel.
            attrs_to_bake.remove('ikTwist')
        if 'ikfk_switch' in attrs_to_bake:
            # We don't want keys on this unless it's intentional.
            attrs_to_bake.remove('ikfk_switch')
        if 'follow' in attrs_to_bake:
            # Pitch the multiconstraint follow attr.
            attrs_to_bake.remove('follow')
        
        if start_frame != end_frame and None not in [start_frame, end_frame]:
            baking.bake_objects(things_to_bake, custom_attrs=attrs_to_bake, bake_range=[start_frame, end_frame])
        else:
            if start_frame:
                cmds.currentTime(start_frame)
            pm.setKeyframe(things_to_bake)
        pm.delete(things_to_delete)
    

    @ma_decorators.keep_autokey_decorator
    #@ma_decorators.keep_current_frame_decorator
    @ma_decorators.keep_selection_decorator
    @ma_decorators.keep_namespace_decorator
    def mirror_rig(self, start_frame=None, end_frame=None):
        # Disable autokey
        flag_pynode_list = [x.pynode for x in self.get_all_flags()]
        if None in time_utils.get_keyframe_range_from_nodes(flag_pynode_list):
            logger.error('No keyframes were found on flags, we\'re going to bail')
            return
        cmds.autoKeyframe(state=False)

        # Step one, create a mirror namespace so we can purge it later.
        mirror_namespace = string_utils.generate_random_string()
        namespace_utils.set_namespace(mirror_namespace)

        asset_id = self.asset_id
        skeleton_path = assetlist.get_asset_by_id(asset_id).skeleton_path
        if not skeleton_path or not os.path.exists(skeleton_path):
            return

        # Step two, get our current pose or our full animation
        driver_root = self.bake_rig_to_skeleton(start_frame, end_frame, set_to_zero=False)
        driver_skel_hierarchy = joint_utils.SkeletonHierarchy(driver_root)

        # Step three, zero our skeleton and build our reverse attachment.
        rev_root = pm.duplicate(driver_root, upstreamNodes=True, returnRootsOnly=True)[0]
        
        mirror_group = pm.group(n='mirror_grp', em=True, w=True)
        rev_root.setParent(mirror_group)
        rev_skel_hierarchy = joint_utils.SkeletonHierarchy(rev_root)
        for skel_root in [rev_root, driver_root]:
            logger.debug(f'Setting {skel_root} to bind')
            joint_utils.reset_bind_pose(skeleton_path, skel_root)

        mirror_group.sx.set(-1)
        final_root = joint_utils.import_skeleton(skeleton_path)
        final_skel_hierarchy = joint_utils.SkeletonHierarchy(final_root)

        # Step four, attach our two skeletons using naming conventions to invert.
        # If the rig is not symmetrical this could end up pretty weird.
        count = 0
        for driver_joint_name, driver_joint in driver_skel_hierarchy.skel_hierarchy.items():
            count += 1
            if driver_joint_name.endswith('_lt'):
                rev_joint_name = driver_joint_name[:-3] + '_rt'
            elif driver_joint_name.endswith('_rt'):
                rev_joint_name = driver_joint_name[:-3] + '_lt'
            else:
                rev_joint_name = driver_joint_name

            rev_joint = rev_skel_hierarchy.skel_hierarchy.get(rev_joint_name, None)
            fin_joint = final_skel_hierarchy.skel_hierarchy.get(driver_joint_name, None)

            if pymaths.get_vector_length(pymaths.sub_vectors(pm.xform(driver_joint, q=True, ws=True, t=True), pm.xform(rev_joint, q=True, ws=True, t=True))) < 2:
                constraint_utils.parent_constraint_safe(rev_joint, fin_joint, mo=True)
            else:
                logger.warning(f'{driver_joint_name} was not mirrored as a reverse joint was not found within range.')
                constraint_utils.parent_constraint_safe(driver_joint, fin_joint)

        # Step five, Baking!
        namespace_utils.set_namespace('')
        self.bake_skeleton_to_rig(final_root, start_frame, end_frame, append=False, motion_encode=False)

        # Step six, cleanup
        namespace_utils.purge_namespace(mirror_namespace)


class FRAGComponent(frag_base.FRAGNode):
    # Anything rig related
    # These can be helpers like twist components
    _version = 1.0

    @classmethod
    def create(cls, frag_parent, side=None, region=None, alignment_node=None, **kwargs):
        if not isinstance(frag_parent, FRAGRig):
            (f'{frag_parent}, FRAGNode parent must be a FRAGRig')
            return
        
        new_frag_node = super().create(frag_parent=frag_parent, **kwargs)
        if side: new_frag_node.side = side
        if region: new_frag_node.region = region

        if alignment_node and isinstance(alignment_node, pm.nt.Transform):
            # if we have an alignment object snap our do not touch group and lock the transforms
            do_not_touch_group = new_frag_node.add_do_not_touch_group()
            pm.delete(pm.parentConstraint(alignment_node, do_not_touch_group, w=True, mo=False))
            attr_utils.set_attr_state(do_not_touch_group)
        return new_frag_node

    def remove(self):
        pm.delete([self.do_not_touch_group, self.pynode])

    @property
    def side(self):
        if self.pynode.hasAttr('side'):
            return self.pynode.getAttr('side')

    @side.setter
    def side(self, val):
        if not self.pynode.hasAttr('side'):
            self.pynode.addAttr('side', dt='string')
        self.pynode.setAttr('side', val)

    @property
    def region(self):
        if self.pynode.hasAttr('region'):
            return self.pynode.getAttr('region')

    @region.setter
    def region(self, val):
        if not self.pynode.hasAttr('region'):
            self.pynode.addAttr('region', dt='string')
        self.pynode.setAttr('region', val)

    @property
    def frag_rig(self):
        return self.frag_parent

    @property
    def do_not_touch_group(self):
        if self.pynode.hasAttr('do_not_touch_group'):
            return self.pynode.getAttr('do_not_touch_group')

    @do_not_touch_group.setter
    def do_not_touch_group(self, do_not_touch_group):
        self.connect_node(do_not_touch_group, 'do_not_touch_group', 'frag_parent')

    def add_do_not_touch_group(self):
        do_not_touch_group = self.do_not_touch_group
        if not self.do_not_touch_group:
            do_not_touch_group = self._create_managed_group(f'NT_{self.__class__.__name__}_{self.side}_{self.region}')
            do_not_touch_group.setParent(self.frag_parent.add_do_not_touch_group())
            do_not_touch_group.v.set(False)

            self.do_not_touch_group = do_not_touch_group
        return do_not_touch_group

    def attach_component(self, parent_object_list, point=True, orient=True, **kwargs):
        if not parent_object_list or not any([point, orient]):
            return

        if not isinstance(parent_object_list, list):
            parent_object_list = [parent_object_list]
        parent_object_list = [x if not isinstance(x, flags.Flag) else x.pynode for x in parent_object_list]

        nt_grp = self.do_not_touch_group
        if nt_grp:
            if point:
                pm.delete(pm.listConnections(nt_grp.tx, type=pm.nt.Constraint))
            if orient:
                pm.delete(pm.listConnections(nt_grp.rx, type=pm.nt.Constraint))

            attr_utils.set_attr_state(nt_grp, False, attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS)

        if point:
            constraint_utils.parent_constraint_safe(parent_object_list, nt_grp, mo=1, skip_rotate_attrs=['x', 'y', 'z'])
            self.connect_nodes(parent_object_list, 'point_attach_objects')

        if orient:
            constraint_utils.parent_constraint_safe(parent_object_list, nt_grp, mo=1, skip_translate_attrs=['x', 'y', 'z'])
            self.connect_nodes(parent_object_list, 'orient_attach_objects')

        attr_utils.set_attr_state(nt_grp, True, attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS)
        
    def get_build_kwargs(self):
        """
        Gets a dictionary of kwargs that represent the build args of a component and their values on creation.

        :return: A dictionary of the names of kwargs for the component's build and their values on creation
        :rtype: dict{}
        """

        return_dict = {}
        if self.pynode.hasAttr('buildKwargs'):
            for attr in self.pynode.buildKwargs.children():
                attr_name = attr.attrName()
                if not attr_name.endswith('_hidden'):
                    return_dict[attr_name.replace('buildKwargs_', '')] = attr.get()
        return return_dict

    def serialize_component(self, skel_hierarchy=None):
        """
        Converts a rig component into a dictionary of build instructions for regeneration later.

        At the top of our dict we have some lookup information for the component.
        {
            'frag_type'
            'side'
            'region'
            Next we have a nested dict that includes all of the build kwargs.
            'build_kwargs':{
                            'start_joint',
                            'end_joint',
                            'joint_chain',
                            **kwargs
                            }
            Parallel the build_kwargs we have attachment info if it has an attach type it'll include the nodes associated with it.
            'attachments':{
                           'point': [{
                                    OBJECT_IDENTIFIER_DICT
                                    }]
                           'orient': [{
                                    OBJECT_IDENTIFIER_DICT
                                    }],
                          }
            Finally an optional entry about the flag data, they key for the dict is the flag index, we use this to reassign data later.
            'flags':{
                    1:{
                      'locked_attrs': ['tx', ...]
                      'rotate_order': int
                      'multiconstraint': {MULTICONSTRAINT_SERIALIZED_DATA}
                      }
                    }
        }

        :return: A dictionary containing all notable information to recreate this instance of a rig component.
        :rtype: dict{}
        """
        if not skel_hierarchy:

            root_joint = self.get_frag_root().root_joint
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        data_dict = {}
        # Component type and side/region lookup.
        data_dict['component'] = {}
        data_dict['component']['frag_type'] = self.frag_type
        data_dict['component']['side'] = self.side
        data_dict['component']['region'] = self.region

        # Lets get our build kwargs
        data_dict['build_kwargs'] = {}
        # Handle our joints
        bind_chain = self.joints
        if bind_chain:
            data_dict['build_kwargs']['joint_chain'] = [get_object_identifier(x) for x in bind_chain]
            data_dict['build_kwargs']['start_joint'] = data_dict['build_kwargs']['joint_chain'][0]
            data_dict['build_kwargs']['end_joint'] = data_dict['build_kwargs']['joint_chain'][-1]
        data_dict['build_kwargs'] = {**data_dict['build_kwargs'], **self.get_build_kwargs()}

        # How is this component attached to another?
        data_dict['attachments'] = {}
        parent_attach_node_list = []
        for attach_type in ['point', 'orient']:
            attr_name = f'{attach_type}_attach_objects'
            if self.pynode.hasAttr(attr_name):
                parent_attach_node_list = [get_object_identifier(node, skel_hierarchy) for node in self.pynode.getAttr(attr_name)]
                data_dict['attachments'][attach_type] = parent_attach_node_list

        # flags data, this is optional
        if isinstance(self, FRAGAnimatedComponent):
            # we have a rig component with flags.
            # this handles any multiconstraints attached to this rig component.
            flag_data_dict = {}
            flag_node_list = self.flags
            for index, wrapped_flag in enumerate(flag_node_list):
                flag_pynode = wrapped_flag.pynode
                current_flag_dict = {}
                attr_lock_list = []
                for attr_name in attr_utils.TRANSFORM_ATTRS:
                    if flag_pynode.attr(attr_name).isLocked():
                        attr_lock_list.append(attr_name)
                current_flag_dict['locked_attrs'] = attr_lock_list
                flag_rotate_order = flag_pynode.rotateOrder.get()
                if flag_rotate_order:
                    flag_data_dict['rotate_order'] = flag_rotate_order
                if wrapped_flag.pynode.hasAttr('source_multi_constraint'):
                    multiconstraint_component = frag_base.FRAGNode(wrapped_flag.pynode.source_multi_constraint.get())
                    target_list = multiconstraint_component.pynode.targets.get()
                    if len(target_list) > 1:
                        multiconstraint_data, skel_hierarchy = multiconstraint_component.serialize_component(skel_hierarchy)
                        current_flag_dict['multiconstraint'] = multiconstraint_data
                flag_data_dict[index] = current_flag_dict
            data_dict['flags'] = flag_data_dict
        return data_dict, skel_hierarchy


class FRAGAnimatedComponent(FRAGComponent):
    # Specifically any components that have animatable flags.
    # These should know how to leash to a skeleton and bake between.
    @classmethod
    def create(cls, frag_parent, side=None, region=None, alignment_node=None, **kwargs):
        if not isinstance(frag_parent, FRAGRig):
            (f'{frag_parent}, FRAGNode parent must be a FRAGRig')
            return

        new_frag_node = super().create(frag_parent=frag_parent, side=side, region=region, alignment_node=alignment_node, **kwargs)
        return new_frag_node


    def remove(self):
        pm.delete([self.do_not_touch_group, self.flags_group, self.pynode])

    @property
    def joints(self):
        if self.pynode.hasAttr('joints'):
            return self.pynode.getAttr('joints')
        return []

    @property
    def flags_group(self):
        if self.pynode.hasAttr('flags_group'):
            return self.pynode.getAttr('flags_group')

    @flags_group.setter
    def flags_group(self, flags_group):
        self.connect_node(flags_group, 'flags_group', 'frag_parent')

    def add_flags_group(self):
        flags_group = self.flags_group
        if not self.flags_group:
            flags_group = self._create_managed_group(f'flags_{self.__class__.__name__}_{self.side}_{self.region}')
            flags_group.setParent(self.frag_parent.add_flags_group())

            self.flags_group = flags_group
        return flags_group

    @property
    def flags(self):
        if self.pynode.hasAttr('flags'):
            flag_list = self.pynode.getAttr('flags')
            return [flags.Flag(x) for x in flag_list]

    def attach_component(self, parent_object_list, point=True, orient=True, **kwargs):
        if not parent_object_list or not any([point, orient]):
            return

        if not isinstance(parent_object_list, list):
            parent_object_list = [parent_object_list]
        parent_object_list = [x if not isinstance(x, flags.Flag) else x.pynode for x in parent_object_list]

        nt_grp = self.do_not_touch_group
        flags_group = self.flags_group
        for rig_group in [nt_grp, flags_group]:
            if rig_group:
                if point:
                    pm.delete(pm.listConnections(rig_group.tx, type=pm.nt.Constraint))
                if orient:
                    pm.delete(pm.listConnections(rig_group.rx, type=pm.nt.Constraint))

                attr_utils.set_attr_state(rig_group, False, attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS)

        if point:
            constraint_utils.parent_constraint_safe(parent_object_list, nt_grp, mo=1, skip_rotate_attrs=['x', 'y', 'z'])
            constraint_utils.parent_constraint_safe(parent_object_list, flags_group, mo=1, skip_rotate_attrs=['x', 'y', 'z'])
            self.connect_nodes(parent_object_list, 'point_attach_objects')

        if orient:
            constraint_utils.parent_constraint_safe(parent_object_list, nt_grp, mo=1, skip_translate_attrs=['x', 'y', 'z'])
            constraint_utils.parent_constraint_safe(parent_object_list, flags_group, mo=1, skip_translate_attrs=['x', 'y', 'z'])
            self.connect_nodes(parent_object_list, 'orient_attach_objects')

        attr_utils.set_attr_state(nt_grp, True, attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS)

    def attach_to_skeleton(self, root_joint, skel_hierarchy=None, *args, **kwargs):
        if not root_joint:
            return None, []
        
        if not skel_hierarchy:
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        bind_chain = skel_hierarchy.get_full_chain(self.side, self.region)
        return_list = []
        for bind_joint, frag_flag in zip(bind_chain, self.flags):
            flag_pynode = frag_flag.pynode
            return_list.append(constraint_utils.parent_constraint_safe(bind_joint, flag_pynode))
            for attr_name in attr_utils.SCALE_ATTRS:
                if flag_pynode.attr(attr_name).isSettable():
                    flag_pynode.attr(attr_name) >> flag_pynode.attr(attr_name)
        return skel_hierarchy, return_list

    def get_bakeable_rig_nodes(self):
        """
        Returns a list of bakeable flags and the helpers/constraints driving them.

        :return: A list of transforms, keyable attrs, and things to remove after baking.
        :rtype: list[Transform], list[str] list[PyNode]
        """
        flag_list = self.flags
        things_to_delete = []
        attr_list = []
        bakeable_flags = []
        for wrapped_flag in flag_list:
            flag_pynode = wrapped_flag.pynode
            constraint_list = flag_pynode.getChildren(type=pm.nt.ParentConstraint)
            for constraint_node in constraint_list:
                things_to_delete += [x for x in constraint_utils.get_constraint_targets(constraint_node) if hasattr(x, 'bake_helper')]
            things_to_delete += constraint_list
            # only return attributes with an incoming connection
            attr_list += [x.attrName() for x in flag_pynode.listAttr(ud=True, keyable=True, settable=True)]
            if constraint_list or attr_list:
                bakeable_flags.append(flag_pynode)

        return bakeable_flags, attr_list, things_to_delete

    def set_scale(self):
        """
        overridable function to handle this component's scale attachment settings.

        """
        pass

class FRAGAnimatedComponentSingle(FRAGAnimatedComponent):
    # Specifically any components that have animatable flags, but can only have a single of this type.
    # These should know how to leash to a skeleton and bake between.
    @classmethod
    def create(cls, frag_parent, side=None, region=None, alignment_node=None, **kwargs):
        if not isinstance(frag_parent, FRAGRig):
            (f'{frag_parent}, FRAGNode parent must be a FRAGRig')
            return

        found_frag_node = list_utils.get_first_in_list(frag_parent.get_frag_children(frag_type=cls))
        if found_frag_node:
            return found_frag_node

        new_frag_node = super().create(frag_parent=frag_parent, side=side, region=region, alignment_node=alignment_node, **kwargs)
        return new_frag_node

def get_frag_rig(node):
    frag_root_node = frag_root.get_frag_root(node)
    if frag_root_node:
        return frag_root_node.frag_rig

def get_all_frag_rigs():
    return_list = []
    for frag_root_node in frag_root.get_all_frag_roots():
        frag_rig_node = frag_root_node.frag_rig
        if frag_rig_node:
            return_list.append(frag_rig_node)
    return return_list

def get_component(node):
    if isinstance(node, pm.nt.Network):
        try:
            frag_node = frag_base.FRAGNode(node)
            return frag_node
        except:
            # we have a network node that's not a FRAGNode?
            return
    if isinstance(node, pm.nt.Joint):
        # maybe we have a flag.
        flag_node = flags.is_flag(node)
        if flag_node:
            return flag_node.frag_parent
        else:
            # we have a joint, but it's not a flag.
            if node.hasAttr('fragParent'):
                # if we have frag_parent markup
                frag_parent = node.getAttr('fragParent')
                if frag_parent:
                    return frag_base.FRAGNode(frag_parent)
            
            # if it doesn't have markup lets look for connections
            network_connections = node.listConnections(type=pm.nt.Network)
            for x in network_connections:
                try:
                    frag_node = frag_base.FRAGNode(x)
                    return frag_node
                except:
                    continue

# Rig helper fncs and serialization fncs
@ma_decorators.keep_autokey_decorator
def setup_twist_components(frag_rig, skel_hierarchy=None):
    """
    Purge old twist components and rebuild them.

    :param FRAGRig frag_rig: The FRAGRig to have new twist joints built on.
    """
    # HACK FSchorsch, this gets around a cycle import because of how the FRAG init works.
    from mca.mya.rigging.frag.components import twist_component

    existing_twist_component_list = frag_rig.get_frag_children(frag_type=twist_component.TwistComponent)
    for found_twist_component in existing_twist_component_list:
        if found_twist_component.version != twist_component.TwistComponent._version:
            found_twist_component.remove()

    if not skel_hierarchy:
        frag_root = frag_rig.get_frag_root()
        skel_root = frag_root.root_joint
        skel_hierarchy = joint_utils.SkeletonHierarchy(skel_root)

    cmds.autoKeyframe(state=False)
    frag_rig.zero_flags()
    for _, entry_dict in skel_hierarchy.twist_joints.items():
        for _, data_dict in entry_dict.items():
            twist_component.TwistComponent.create(frag_rig, data_dict['joints'])

def build_serialized_rig(frag_rig, serialized_build_dict):
    """
    From an established frag_Rig, rebuild and attach a list of components.

    :param FRAGRig frag_rig: The frag rig all new components will be attached to.
    :param dict('components':list(dict, ...), 'version':float) serialized_build_dict: A dictionary containing a list of dictionaries which contain the data required to build components.
    """
    frag_root = frag_rig.get_frag_root()
    root_joint = frag_root.root_joint
    skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

    flags_path = None
    try:
        asset_id = frag_rig.get_frag_root().asset_id
        mca_asset = assetlist.get_asset_by_id(asset_id)
        if mca_asset:
            flags_path = mca_asset.flags_path
    except:
        pass
    
    existing_components_dict = {}
    for rig_component in frag_rig.get_frag_children(frag_type=FRAGComponent):
        component_side = rig_component.side
        component_region = rig_component.region
        if component_side not in existing_components_dict:
            existing_components_dict[component_side] = []
        existing_components_dict[component_side].append(component_region)
    if not existing_components_dict:
        frag_rig.rig_version = serialized_build_dict.get('version', 1.0)

    # Build the new components, return any multiconstraints and attach params, we'll handle those after the fact.
    multiconstraint_list = []
    components_attachment_dict = {}
    for data_dict in serialized_build_dict.get('components', []):
        component_data = data_dict.get('component')
        component_side = component_data.get('side')
        component_region = component_data.get('region')

        # Pass if we've already got a component with the same side/region combo.
        if component_side in existing_components_dict:
            if component_region in existing_components_dict[component_side]:
                continue

        new_component, skel_hierarchy, flag_multiconstraint_list, attachment_data_dict = build_serialized_component(frag_rig, data_dict, skel_hierarchy)
        if not new_component:
            continue
        multiconstraint_list += flag_multiconstraint_list
        if attachment_data_dict:
            components_attachment_dict[new_component] = attachment_data_dict

    # Handle attachments.
    for new_component, attachment_data_dict in components_attachment_dict.items():
        attach_serialized_component(new_component, attachment_data_dict, skel_hierarchy)
    
    # Handle found multiconstraints.
    for multiconstraint_data in multiconstraint_list:
        build_serialized_component(frag_rig, multiconstraint_data, skel_hierarchy)            

    frag_rig.finish_rig(flags_path)
    setup_twist_components(frag_rig, skel_hierarchy)


def build_serialized_component(frag_rig, data_dict, skel_hierarchy=None):
    """
    From a build dict create a new component based on those specifications then attach it to the indicated FRAGRig

    :param FRAGRig frag_rig: The frag rig all new components will be attached to.
    :param dict data_dict: A dictionary containing the information required to build new components.
    :param SkeletonHierarchy skel_hierarchy: The ChainMarkup representing the skeleton associated with the frag rig.
        By providing this it reduces the time to build. Otherwise, we'll derive it from the passed FRAGRig.
    :return: The new component, and it's attach dictionary. The attach dictionary is used to attach the newly built
        component after all components have been rebuilt. This is to ensure components that have dependencies on other
        components attach correctly.
    :rtype FRAGComponent, dict
    """
    if not skel_hierarchy:
        frag_root = frag_rig.get_frag_root()
        root_joint = frag_root.root_joint
        skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

    component_type = data_dict.get('component', {}).get('frag_type')

    component_build_class = frag_base.FRAGNodeRegister._FRAGNODE_TYPES.get(component_type)
    if not component_build_class:
        logger.error(f'{component_type}: Is not a registered FRAG type.')
        return None, None, [], {}
    
    # Convert identifier kwargs into actual scene objects.
    kwargs_dict = data_dict.get('build_kwargs', {})
    for arg_name, arg_val in kwargs_dict.items():
        if isinstance(arg_val, dict):
            found_object = get_object_from_identifiers(frag_rig, arg_val, skel_hierarchy)
            kwargs_dict[arg_name] = found_object if found_object else None
        elif arg_val and isinstance(arg_val, list) and isinstance(arg_val[0], dict):
            return_list_value = [get_object_from_identifiers(frag_rig, x, skel_hierarchy) for x in arg_val]
            return_list_value = [x for x in return_list_value if x]
            kwargs_dict[arg_name] = return_list_value if return_list_value else []

    # Build component
    new_component = component_build_class.create(frag_rig, **kwargs_dict)
    if not new_component:
        return None, None, [], {}

    # Handle Attachment
    attachment_data_dict = data_dict.get('attachments', {})

    # Handle flags
    multiconstraint_list = []
    if isinstance(new_component, FRAGAnimatedComponent):
        flags_data_dict = data_dict.get('flags', {})
        for index, wrapped_flag in enumerate(new_component.flags):
            flag_data = flags_data_dict.get(index, {}) or flags_data_dict.get(0, {})
            if not flag_data:
                continue

            flag_pynode = wrapped_flag.pynode

            # Locked attributes
            locked_attr_list = flag_data.get('locked_attrs')
            if locked_attr_list:
                # $HACK set them all to visible then lock attrs. Due to certain build flags and post
                # build settings on flags we can create holes.
                wrapped_flag.set_attr_state(False)
                wrapped_flag.set_attr_state(attr_list=flag_data.get('locked_attrs'))
            
            # Rotate order
            flag_rotate_order = flag_data.get('flag_rotate_order', 0)
            if flag_rotate_order:
                flag_pynode.setAttr('rotateOrder', flag_rotate_order)

            # If it had a multiconstraint append it to the list for later.
            multiconstraint_data = flag_data.get('multiconstraint')
            if multiconstraint_data:
                multiconstraint_list.append(multiconstraint_data)

    return new_component, skel_hierarchy, multiconstraint_list, attachment_data_dict


def attach_serialized_component(rig_component, attach_dict, skel_hierarchy=None):
    """
    Attach the component based on the serialized attach dict. This should always be run after all components have been
    built, as the attach can include flags from other components.

    :param FRAGComponent rig_component: The FRAG component that will be attached.
    :param dict attach_dict: A dictionary of kwargs for the attach process, and identifiers for the objects used in it.
    :param SkeletonHierarchy skel_hierarchy: The SkeletonHierarchy representing the skeleton associated with the frag rig.
        By providing this it reduces the time to build. Otherwise, we'll derive it from the passed FRAGRig.
    :return:
    """
    frag_rig = rig_component.frag_rig
    if not skel_hierarchy:
        frag_root = frag_rig.get_frag_root()
        root_joint = frag_root.root_joint
        skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

    point_object_list = [get_object_from_identifiers(frag_rig, x, skel_hierarchy) for x in attach_dict.get('point', [])]
    orient_object_list = [get_object_from_identifiers(frag_rig, x, skel_hierarchy) for x in attach_dict.get('orient', [])]

    if point_object_list:
        point = True
    if orient_object_list:
        orient = True

    if not point_object_list and not orient_object_list:
        return
    
    if collections.Counter(point_object_list) == collections.Counter(orient_object_list):
        # If our attach points are the same set them at the same time:
        rig_component.attach_component(parent_object_list=point_object_list, point=point, orient=orient)
    else:
        rig_component.attach_component(parent_object_list=point_object_list, point=point, orient=False)
        rig_component.attach_component(parent_object_list=orient_object_list, point=False, orient=orient)


def get_object_identifier(node, skel_hierarchy=None):
    """

    :param Transform node: A Maya transform node representing either a joint, or flag.
    :param SkeletonHierarchy skel_hierarchy: The SkeletonHierarchy representing the skeleton associated with the frag rig.
        By providing this it reduces the time to build. Otherwise, we'll derive it from the passed Joint.
    :return: A dictionary containing lookup identifiers for finding this object locally to the rig.
    :rtype: dict
    """
    return_dict = {}
    wrapped_flag = flags.is_flag(node)
    if wrapped_flag:
        flag_component = wrapped_flag.frag_parent
        flag_list = [x.pynode for x in flag_component.flags]
        return_dict['type'] = 'flag'
        return_dict['side'] = flag_component.side
        return_dict['region'] = flag_component.region
        if node == flag_list[-1]:
            object_index = -1
        else:
            object_index = flag_list.index(node)
        return_dict['index'] = object_index
    elif isinstance(node, pm.nt.Joint):
        wrapped_joint = joint_utils.JointMarkup(node)
        return_dict['type'] = 'skeleton'
        return_dict['side'] = wrapped_joint.side
        return_dict['region'] = wrapped_joint.region
        if not skel_hierarchy:
            root_joint = dag_utils.get_absolute_parent(node, pm.nt.Joint)
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)
        joint_list = skel_hierarchy.get_full_chain(wrapped_joint.side, wrapped_joint.region)
        if node == joint_list[-1]:
            object_index = -1
        else:
            object_index = joint_list.index(node)
        return_dict['index'] = object_index
    else:
        # If it's not a concrete data type we can save it as a string, and blindly try and recover it.
        return_dict['type'] = 'named_object'
        return_dict['name'] = naming.get_basename(node)
    return return_dict


def get_object_from_identifiers(frag_rig, identifier_dict, skel_hierarchy=None):
    """
    From a dictionary of identifiers find the object local to the given FRAG rig that matches them.

    :param FRAGRig frag_rig: The frag rig to use as the local lookup for the object.
    :param dict identifier_dict: A dictionary containing lookup identifiers for finding this object locally to the rig.
    :param SkeletonHierarchy skel_hierarchy: The ChainMarkup representing the skeleton associated with the frag rig.
        By providing this it reduces the time to build. Otherwise, we'll derive it from the passed Joint.
    :return: The found object
    :rtype: Transform
    """
    object_type = identifier_dict.get('type')
    if object_type == 'flag':
        rig_component = list_utils.get_first_in_list(frag_rig.get_frag_children(side=identifier_dict.get('side'), region=identifier_dict.get('region')))
        if rig_component:
            flag_list = rig_component.flags
            object_index = identifier_dict.get('index', 0)
            if flag_list:
                return flag_list[object_index] if len(flag_list) > object_index else flag_list[0]
    elif object_type == 'skeleton':
        if not skel_hierarchy:
            frag_root = frag_rig.get_frag_root()
            root_joint = frag_root.root_joint
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)
        skel_chain = skel_hierarchy.get_full_chain(identifier_dict.get('side'), identifier_dict.get('region'))
        object_index = identifier_dict.get('index', 0)
        if skel_chain:
            return skel_chain[object_index] if len(skel_chain) > object_index else skel_chain[0]
    elif object_type == 'named_object':
        return list_utils.get_first_in_list(pm.ls(identifier_dict.get('name')))


def save_serialized_rig(frag_rig, rig_path):
    """
    From a given FRAG Rig, serialize the build instructions for each component, and save them to the given path.

    :param FRAGRig frag_rig: A FRAG Rig that represents the rig to be serialized.
    :param str rig_path: The full path to where the rig build instructions should be saved.
    """
    if not frag_rig:
        # A frag rig is requried to continue
        return

    if not rig_path or not rig_path.endswith('.rig'):
        # A valid path must be provided.
        return

    serialized_build_dict = frag_rig.serialize_rig(increment_version=True)
    if not serialized_build_dict:
        # failed to serialize rig.
        return

    fileio.touch_path(rig_path)
    yamlio.write_yaml(rig_path, serialized_build_dict)


def load_serialized_rig(frag_rig, rig_path):
    """
    For a FRAG Rig and a given path, load and build the serialized rig.

    :param FRAGRig frag_rig: The FRAG Rig which the serialized rig will attempt to be built on.
    :param str rig_path: The full path to where the rig build instructions are.
    """
    if not rig_path or not os.path.exists(rig_path):
        return

    if not frag_rig:
        return

    serialized_build_dict = yamlio.read_yaml(rig_path) or {}

    build_serialized_rig(frag_rig, serialized_build_dict)
    if not frag_rig.rig_file:
        frag_rig.rig_file = os.path.basename(rig_path)
# End Serializing rigs

@ma_decorators.undo_decorator
def attach_rigs(driver_rig, attached_rig):
    """
    From the two given rigs, match up their components by side and region then constrain their flags.

    :param FRAGRig driver_rig: The FRAGRig that will drive the pair of rigs.
    :param FRAGRig attached_rig: The FRAGRIG that will be puppeted by the driver rig.
    """
    if attached_rig.pynode.hasAttr('attached_to') and attached_rig.pynode.getAttr('attached_to'):
        logger.warning(f'{attached_rig.get_frag_root().asset_name} already has a driver rig.')
        return

    driver_rig_dict = {}
    for rig_component in driver_rig.get_frag_children():
        rig_type = rig_component.frag_type
        if rig_type == 'MultiConstraintComponent':
            continue
        rig_side = rig_component.side
        rig_region = rig_component.region
        if rig_side and rig_region:
            if rig_side not in driver_rig_dict:
                driver_rig_dict[rig_side] = {}
            driver_rig_dict[rig_side][rig_region] = rig_component

    for rig_component in attached_rig.get_frag_children(frag_type=FRAGAnimatedComponent):
        rig_side = rig_component.side
        rig_region = rig_component.region
        driver_component = driver_rig_dict.get(rig_side, {}).get(rig_region, None)
        if driver_component:
            logger.debug(f'found {driver_component}')
            try:
                driver_flags = driver_component.flags
                driven_flags = rig_component.flags

                do_name_check = True if len(driver_flags) != len(driven_flags) else False
                for driver_flag, attach_flag in zip(driver_flags, driven_flags):
                    driver_flag_name, attach_flag_name = map(lambda x: naming.get_basename(x.pynode), [driver_flag, attach_flag])
                    driver_node_namespace = naming.get_node_name_parts(driver_flag.pynode)[1]

                    if driver_flag_name != attach_flag_name and do_name_check:
                        driver_flag_names = list(map(lambda x: naming.get_basename(x.pynode), driver_flags))
                        driver_flag = next((x for x in driver_flag_names if x == attach_flag_name))
                        if driver_node_namespace:
                            driver_flag = f'{driver_node_namespace}:{driver_flag}'

                    constraint_utils.parent_constraint_safe(driver_flag.pynode, attach_flag.pynode)
                    attach_flag.align_group.v.set(False)
            except:
                pass

    if not attached_rig.pynode.hasAttr('attached_to'):
        attached_rig.pynode.addAttr('attached_to', at='message')
    driver_rig.pynode.message >> attached_rig.pynode.attached_to


@ma_decorators.undo_decorator
def detach_rig(attached_rig, bake_animation, start_frame=None, end_frame=None):
    """
    Remove the connection between the driver and driven rigs. Optionally bake down the animation.

    :param FRAGRig attach_rig: The rig being driven in an attached rig system.
    :param bool bake_animation: If the animation should be baked down to the attached rig.
    :param int start_frame: The first frame in the bake range.
    :param int end_frame: The last frame in the bake range.
    """
    attached_flags = []
    custom_attr_list = []
    constraint_list = []
    if attached_rig.pynode.hasAttr('attached_to') and attached_rig.pynode.getAttr('attached_to'):
        driver_rig = frag_base.FRAGNode(attached_rig.pynode.getAttr('attached_to'))
        for flag_node in attached_rig.get_all_flags():
            if not flag_node.pynode.hasAttr('overdriven_by') or not flag_node.pynode.getAttr('overdriven_by'):
                attached_flags.append(flag_node)
                constraint_list += flag_node.pynode.getChildren(type=pm.nt.Constraint)
                flag_group = flag_node.pynode.getParent()
                flag_group.setAttr('v', True)
                for attr in flag_node.pynode.listAttr(ud=True, k=True, se=True):
                    attr_name = attr.attrName()
                    if 'blendParent' not in attr_name:
                        custom_attr_list.append(attr_name)
    else:
        logger.warning(f'{attached_rig.get_frag_root().asset_name} is not attached to another rig.')
        return

    if not constraint_list:
        return

    if attached_flags and bake_animation:
        if not start_frame or not end_frame:
            frame_range = time_utils.get_times([x.pynode for x in driver_rig.pynode.get_all_flags()])
            start_frame = start_frame or frame_range[0]
            end_frame = end_frame or frame_range[1]
        baking.bake_objects(attached_flags, custom_attrs=list(set(custom_attr_list)), bake_range=[start_frame, end_frame])

    pm.delete(constraint_list)
    attached_rig.pynode.disconnectAttr('attached_to')
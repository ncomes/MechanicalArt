"""
Modules that contains important fncs for serializing and loading serialized rigs.
"""
# System global imports
import os
import time
import datetime
# software specific imports
import pymel.core as pm

# PySide2 imports
from PySide2.QtWidgets import QFileDialog

#  python imports
from mca.common import log
from mca.common.assetlist import assetlist
from mca.common.textio import yamlio
from mca.common.utils import fileio, lists
from mca.common.paths import project_paths

from mca.mya.rigging import frag, chain_markup, rig_utils
from mca.mya.rigging.flags import frag_flag
from mca.mya.utils import attr_utils, dag, naming
from mca.mya.pyqt import dialogs

logger = log.MCA_LOGGER


class ReadRigData:
    def __init__(self, build_list):
        self._build_list = build_list

    @property
    def build_list(self):
        return self._build_list

    @classmethod
    def load(cls, full_rig_path):
        """
        Loads a .rig from a file path.

        :param str full_rig_path:  The .rig file.
        :return: Returns the serialized rig data.
        :rtype: ReadRigData
        """

        if not os.path.exists(full_rig_path):
            logger.warning(f'Could not find rig file at "{full_rig_path}".')
            return
        # load the rig data
        serialized_build_list = yamlio.read_yaml_file(full_rig_path) or []

        return cls(build_list=serialized_build_list)

    @property
    def version(self):
        return self.build_list.get('version', 1)

    @version.setter
    def version(self, value):
        self._build_list.update({'version': value})



class ComponentBuildData:
    def __init__(self, component_data):
        self._component_data = component_data

    @property
    def component_data(self):
        return self._component_data











class FlagBuildData:
    """
    Class that holds data for a flag.  This is for serializing and deserializing a flag for a rig or build-a-rig.
    """

    def __init__(self, flag):
        self._flag = flag

    @property
    def flag(self):
        """
        Returns the flag node.
        """

        return self._flag

    @property
    def name(self):
        """
        Returns the flag name.
        """

        return self.flag.name

    @property
    def locked_attrs(self):
        """

        """
        attr_list = []
        for attr_name in attr_utils.TRANSFORM_ATTRS:
            attr_list.append([attr_name, self.flag.attr(attr_name).isLocked()])
        return attr_list

    @property
    def flag_types(self):
        type_list = []
        for attr_name in frag_flag.FLAG_TYPES:
            if self.flag.hasAttr(attr_name) and self.flag.getAttr(attr_name):
                type_list.append(attr_name)
        return type_list


class FRAGComponentData:
    def __init__(self, frag_component, skel_hierarchy=None):
        self._frag_component = frag.FRAGNode(frag_component)
        self.frag_rig = frag.get_frag_rig(self._frag_component)
        self.skel_hierarchy = skel_hierarchy
        if not skel_hierarchy:
            self.skel_heirarchy = self.get_skel_hierarchy()

    def get_skel_hierarchy(self):
        frag_root = self.frag_rig.get_root()
        skel_root = frag_root.root_joint
        return chain_markup.ChainMarkup(skel_root)

    @property
    def frag_component(self):
        return self._frag_component

    @property
    def side(self):
        return self.frag_component.side

    @property
    def region(self):
        return self.frag_component.region

    @property
    def name(self):
        name = naming.get_basename(self.frag_component)
        return name

    @property
    def build_kwargs(self):
        return self.frag_component.get_build_kwargs()

    @property
    def component_type(self):
        return self.frag_component.get_type()

    @property
    def version(self):
        return self.frag_component.VERSION

    @property
    def source_objects(self):
        if not isinstance(self.frag_component, frag.MultiConstraint):
            return
        source_object = self.frag_component.get_source_object()
        return get_object_identifier(source_object, self.skel_hierarchy)

    @property
    def target_objects(self):
        if not isinstance(self.frag_component, frag.MultiConstraint):
            return
        target_list = self.frag_component.get_targets()
        return [get_object_identifier(x, self.skel_hierarchy) for x in target_list]

    @property
    def switch_object(self):
        if not isinstance(self.frag_component, frag.MultiConstraint):
            return
        switch_object = self.frag_component.switchObject.get()
        return get_object_identifier(switch_object, self.skel_hierarchy)

    @property
    def switch_object_default_name(self):
        if not isinstance(self.frag_component, frag.MultiConstraint):
            return
        if self.switch_object and self.switch_object.attr(self.frag_component.get_switch_attr()).getEnums()[0] == 'default':
            return 'default'
        return

    @property
    def start_and_end_joints(self):
        if not isinstance(self.frag_component, frag.RigComponent):
            return
        bind_joints = self.frag_component.bindJoints.get()
        start_joint, end_joint = bind_joints[::len(bind_joints) - 1] if len(bind_joints) > 1 else bind_joints * 2
        start_joint = get_object_identifier(start_joint, self.skel_hierarchy)
        end_joint = get_object_identifier(end_joint, self.skel_hierarchy)
        return start_joint, end_joint

    @property
    def parent_object_list(self):
        if not isinstance(self.frag_component, frag.RigComponent):
            return
        point_attach_objects = self.frag_component.point_object_parents
        orient_attach_objects = self.frag_component.orient_object_parents

        # Merge and grab identifier dicts for each item.
        # These are set together so there can never be a difference in point/orient constraints.
        return [get_object_identifier(x, self.skel_hierarchy) for x in set(point_attach_objects + orient_attach_objects)]

    # GET THE FLAG DATA AND PUSH IT TO THE MAIN CLASS
    def get_all_flags_data(self):
        if not isinstance(self.frag_component, frag.RigComponent):
            return
        flags = []
        for flag in self.frag_component.get_flags():
            flags.append(FlagBuildData(flag))
        return flags


class SerializeRig:
    """
    Class that contains functions that serialize and load serialized rigs.
    """
    def __init__(self, frag_rig, build_list=None):
        self._frag_rig = frag_rig
        self._rig_build_list = build_list or []
        self._version = self.get_version()

    @property
    def frag_rig(self):
        return self._frag_rig

    @property
    def rig_build_list(self):
        return self._rig_build_list

    @property
    def frag_root(self):
        return self.frag_rig.get_root()

    @property
    def skel_root(self):
        return self.frag_root.root_joint

    @property
    def skel_hierarchy(self):
        return chain_markup.ChainMarkup(self.skel_root)

    def get_frag_children(self):
        """
        Returns a list of all the frag components in the current rig.

        :return: A list of all the frag components in the current rig.
        :rtype: list[FRAGRig]
        """

        frag_components = []
        for frag_component in self.frag_rig.get_frag_children():
            if (isinstance(frag_component, frag.TwistFixUpComponent) or
                    not isinstance(frag_component, (frag.RigComponent, frag.MultiConstraint))):
                continue
            frag_components.append(frag_component)
        return frag_components

    @property
    def version(self):
        return self.get_version()

    @version.setter
    def version(self, value):
        self._version = self.set_version(value)

    def set_version(self, version_number=None):
        """
        Set the version number of the current rig.
        """

        if not version_number:
            version_num = 1

        for data_dict in self._rig_build_list:
            for key, value in data_dict.items():
                if key =='version':
                    data_dict.update({'version': version_number})
                    return

        data_dict = {}
        data_dict['version'] = version_number
        self._rig_build_list.append(data_dict)
        return data_dict.get('version', version_number)

    def get_version(self):
        """
        Returns the current version of the rig.
        """

        for data_dict in self._rig_build_list:
            for key, value in data_dict.items():
                if key == 'version':
                    data = data_dict.get(key, 1)
                    return data
        return 1

    def get_component_data(self, component_type):
        data_list = []
        for data_dict in self._rig_build_list:
            for key, value in data_dict.items():
                if key == 'component' and value == component_type:
                    data_list.append(data_dict)
        return data_list

    @staticmethod  # Static method for speed
    def build_data_dict(frag_components, skel_hierarchy):
        """
        From a build rig, serialize all the rig data to dictionaries that contain the information required t
        o rebuild them.

        :param FRAGRig frag_components: Frag rig that represents the rig to be serialized.
        :return: A list of dictionaries containing the information required to rebuild all rig components.
        :rtype: list[dict, ...]
        """

        rig_build_list = []
        for frag_component in frag_components:
            if isinstance(frag_component, frag.TwistFixUpComponent) or not isinstance(frag_component, (
            frag.RigComponent, frag.MultiConstraint)):
                continue

            data_dict = {}
            data_dict['build_kwargs'] = frag_component.get_build_kwargs()
            data_dict['component'] = frag_component.get_type()
            data_dict['build_kwargs']['side'] = frag_component.side
            data_dict['build_kwargs']['region'] = frag_component.region
            if isinstance(frag_component, frag.MultiConstraint):
                source_object = frag_component.get_source_object()
                data_dict['build_kwargs']['source_object'] = get_object_identifier(source_object, skel_hierarchy)
                target_list = frag_component.get_targets()
                data_dict['build_kwargs']['target_list'] = [get_object_identifier(x, skel_hierarchy) for x in
                                                            target_list]
                switch_object = frag_component.switchObject.get()
                data_dict['build_kwargs']['switch_obj'] = get_object_identifier(switch_object, skel_hierarchy)
                if switch_object.attr(frag_component.get_switch_attr()).getEnums()[0] == 'default':
                    data_dict['build_kwargs']['default_name'] = 'default'
            else:
                bind_joints = frag_component.bindJoints.get()
                start_joint, end_joint = bind_joints[::len(bind_joints) - 1] if len(
                    bind_joints) > 1 else bind_joints * 2
                data_dict['build_kwargs']['start_joint'] = get_object_identifier(start_joint, skel_hierarchy)
                data_dict['build_kwargs']['end_joint'] = get_object_identifier(end_joint, skel_hierarchy)

            if isinstance(frag_component, frag.RigComponent):
                data_dict['attach'] = {}
                point_attach_objects = frag_component.point_object_parents
                orient_attach_objects = frag_component.orient_object_parents

                # Merge and grab identifier dicts for each item. These are set together so there can never be a difference in point/orient constraints.
                data_dict['attach']['parent_object_list'] = [get_object_identifier(x, skel_hierarchy) for x in
                                                             set(point_attach_objects + orient_attach_objects)]

                if point_attach_objects:
                    data_dict['attach']['point'] = True
                if orient_attach_objects:
                    data_dict['attach']['orient'] = True

                data_dict['flag'] = []
                for flag in frag_component.get_flags():
                    flag_data = {}
                    attr_list = []
                    flag_data['locked_attrs'] = attr_list
                    for attr_name in attr_utils.TRANSFORM_ATTRS:
                        attr_list.append([attr_name, flag.attr(attr_name).isLocked()])
                    flag_data['flag_types'] = []
                    for attr_name in ['isDetail', 'isSub', 'isContact', 'isUtil']:
                        if flag.hasAttr(attr_name) and flag.getAttr(attr_name):
                            flag_data['flag_types'].append(attr_name)
                    data_dict['flag'].append(flag_data)
            rig_build_list.append(data_dict)
        return rig_build_list

    def serialize_rig(self):
        """
        From a build rig, serialize all the rig data to dictionaries that contain the information required
        to rebuild them.
        """

        time_start = time.time()
        frag_children = self.get_frag_children()
        rig_build_list = self.build_data_dict(frag_components=frag_children, skel_hierarchy=self.skel_hierarchy)
        self._rig_build_list += rig_build_list

        #build_list = serialize_rig(self.frag_rig)  # Using the function outside the class for speed

        time_elapsed = str(datetime.timedelta(seconds=time.time() - time_start))
        logger.debug(f'build_a_data_dict: Time Elapsed: "{time_elapsed}.')
        # self._rig_build_list += build_list
        return self._rig_build_list

    @classmethod
    def save(cls, frag_rig, rig_path):
        """
        From a given FRAG Rig, serialize the build instructions for each component, and save them to the given path.

        :param FRAGRig frag_rig: A FRAG Rig that represents the rig to be serialized.
        :param str rig_path: The full path to where the rig build instructions should be saved.
        :param int version: the rig version number
        """

        if not frag_rig:
            # A frag rig is requried to continue
            return

        if not rig_path or not rig_path.endswith('.rig'):
            # A valid path must be provided.
            return

        version = 1
        if os.path.exists(rig_path):
            data_dict = yamlio.read_yaml_file(rig_path)
            serialized_rig = SerializeRig(frag_rig=frag_rig, build_list=data_dict)
            version = serialized_rig.version + 1

        serialized_rig = SerializeRig(frag_rig=frag_rig)
        serialized_build_list = serialized_rig.serialize_rig()
        serialized_rig.version = version
        if not serialized_build_list:
            logger.warning('failed to serialize rig.')
            return

        fileio.touch_path(rig_path)
        yamlio.write_to_yaml_file(serialized_build_list, rig_path)

    @classmethod
    def load(cls, frag_rig, rig_path):
        if not rig_path or not os.path.exists(rig_path):
            logger.warning(f'Could not find rig file at "{rig_path}".')
            return

        serialized_build_list = yamlio.read_yaml_file(rig_path) or []

        return cls(frag_rig=frag_rig, build_list=serialized_build_list)


def get_object_identifier(node, skel_hierarchy=None):
    """

    :param Transform node: A Maya transform node representing either a joint, or flag.
    :param ChainMarkup skel_hierarchy: The ChainMarkup representing the skeleton associated with the frag rig.
        By providing this it reduces the time to build. Otherwise, we'll derive it from the passed Joint.
    :return: A dictionary containing lookup identifiers for finding this object locally to the rig.
    :rtype: dict
    """

    return_dict = {}
    if frag_flag.is_flag_node(node):
        wrapped_flag = frag_flag.Flag(node)
        flag_component = frag.FRAGNode(wrapped_flag.fragParent.get())
        flag_list = flag_component.get_flags()
        return_dict['type'] = 'flag'
        return_dict['side'] = flag_component.side
        return_dict['region'] = flag_component.region
        if wrapped_flag == flag_list[-1]:
            object_index = -1
        else:
            object_index = flag_list.index(wrapped_flag)
        return_dict['index'] = object_index
    elif isinstance(node, pm.nt.Joint):
        wrapped_joint = chain_markup.JointMarkup(node)
        return_dict['type'] = 'skeleton'
        return_dict['side'] = wrapped_joint.side
        return_dict['region'] = wrapped_joint.region
        if not skel_hierarchy:
            skel_root = dag.get_absolute_parent(node, pm.nt.Joint)
            skel_hierarchy = chain_markup.ChainMarkup(skel_root)
        joint_list = skel_hierarchy.get_full_chain(wrapped_joint.region, wrapped_joint.side)
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


def build_serialized_rig(frag_rig, serialized_build_list):
    """
    From an established frag_Rig, rebuild and attach a list of components.

    :param FRAGRig frag_rig: The frag rig all new components will be attached to.
    :param list[dict, ...] serialized_build_list: A list if dictionaries which contain the data required to build components.
    """

    frag_root = frag_rig.get_root()
    skel_root = frag_root.root_joint
    skel_hierarchy = chain_markup.ChainMarkup(skel_root)

    asset_id = frag_rig.get_root().asset_id
    mca_asset = assetlist.get_asset_by_id(asset_id)
    flag_path = mca_asset.flags_path

    existing_components_dict = {}
    for rig_component in frag_rig.get_frag_children():
        component_side = rig_component.side
        component_region = rig_component.region
        if component_side not in existing_components_dict:
            existing_components_dict[component_side] = []
        existing_components_dict[component_side].append(component_region)

    attach_build_list = []
    multi_constraint_list = []
    for data_dict in serialized_build_list:
        if not data_dict:
            continue
        if data_dict.get('component') == 'MultiConstraint':
            multi_constraint_list.append(data_dict)
            continue

        build_dict = data_dict.get('build_kwargs', {})
        side = build_dict.get('side')
        region = build_dict.get('region')
        if existing_components_dict.get(side):
            if region in existing_components_dict.get(side, []):
                continue
        else:
            existing_components_dict[side] = []

        new_component, attach_dict = build_serialized_component(frag_rig, data_dict, skel_hierarchy)
        if new_component:
            existing_components_dict[side].append(region)
            attach_build_list.append([new_component, attach_dict])
            for my_flag in new_component.get_flags():
                frag_flag.swap_flags([frag_flag.Flag(my_flag)], flag_path)

    for rig_component, attach_dict in attach_build_list:
        pm.objExists(rig_component.node())
        attach_serialized_component(rig_component, attach_dict, skel_hierarchy)

    for data_dict in multi_constraint_list:
        build_dict = data_dict.get('build_kwargs', {})
        side = build_dict.get('side')
        region = build_dict.get('region')
        if existing_components_dict.get(side):
            if region in existing_components_dict.get(side, []):
                continue
        else:
            existing_components_dict[side] = []

        build_serialized_component(frag_rig, data_dict, skel_hierarchy)
        existing_components_dict[side].append(region)

    frag_rig.finalize_rig()
    rig_utils.setup_twist_components(frag_rig)


def build_serialized_component(frag_rig, data_dict, skel_hierarchy=None):
    """
    From a build dict create a new component based on those specifications then attach it to the indicated FRAGRig

    :param FRAGRig frag_rig: The frag rig all new components will be attached to.
    :param dict data_dict: A dictionary containing the information required to build new components.
    :param ChainMarkup skel_hierarchy: The ChainMarkup representing the skeleton associated with the frag rig.
        By providing this it reduces the time to build. Otherwise, we'll derive it from the passed FRAGRig.
    :return: The new component, and it's attach dictionary. The attach dictionary is used to attach the newly built
        component after all components have been rebuilt. This is to ensure components that have dependencies on other
        components attach correctly.
    :rtype: FRAGComponent, dict
    """

    if not skel_hierarchy:
        frag_root = frag_rig.get_root()
        skel_root = frag_root.root_joint
        skel_hierarchy = chain_markup.ChainMarkup(skel_root)

    component_type = data_dict.get('component')
    if not component_type or component_type not in dir(frag):
        return None, None

    for arg_name, arg_val in data_dict.get('build_kwargs', {}).items():
        if isinstance(arg_val, dict):
            found_object = get_object_from_identifiers(frag_rig, arg_val, skel_hierarchy)
            if not found_object:
                # Failed to find a required object.
                return None, None
            data_dict['build_kwargs'][arg_name] = found_object
        elif isinstance(arg_val, list):
            if not arg_val:
                continue
            if isinstance(arg_val[0], dict):
                replace_list = []
                for entry in arg_val:
                    found_object = get_object_from_identifiers(frag_rig, entry, skel_hierarchy)
                    if found_object:
                        replace_list.append(found_object)
                if replace_list:
                    data_dict['build_kwargs'][arg_name] = replace_list

    rig_component = getattr(frag, component_type)
    new_component = rig_component.create(frag_rig, **data_dict.get('build_kwargs', {}))

    if isinstance(new_component, frag.RigComponent):
        flag_data_list = data_dict.get('flag')
        if flag_data_list:
            flag_list = new_component.get_flags()
            for index, flag in enumerate(flag_list):
                if index > len(flag_data_list)-1:
                    continue
                locked_attr_list = [attr_name for attr_name, is_locked in flag_data_list[index].get('locked_attrs', []) if is_locked]
                flag_type_list = flag_data_list[index].get('flag_types', [])
                attr_utils.set_attr_state(flag, attr_list=locked_attr_list, visibility=True)
                for attr_name in flag_type_list:
                    flag.setAttr(attr_name, True)

    return new_component, data_dict.get('attach', {})


def attach_serialized_component(rig_component, attach_dict, skel_hierarchy=None):
    """
    Attach the component based on the serialized attach dict. This should always be run after all components have been
    built, as the attach can include flags from other components.

    :param FRAGComponent rig_component: The FRAG component that will be attached.
    :param dict attach_dict: A dictionary of kwargs for the attach process, and identifiers for the objects used in it.
    :param ChainMarkup skel_hierarchy: The ChainMarkup representing the skeleton associated with the frag rig.
        By providing this it reduces the time to build. Otherwise, we'll derive it from the passed FRAGRig.
    :return:
    """

    frag_rig = rig_component.get_frag_parent()
    if not skel_hierarchy:
        frag_root = frag_rig.get_root()
        skel_root = frag_root.root_joint
        skel_hierarchy = chain_markup.ChainMarkup(skel_root)

    object_list = []
    for lookup_dict in attach_dict.get('parent_object_list', []):
        if not isinstance(lookup_dict, dict):
            object_list.append(lookup_dict)
            continue
        found_object = get_object_from_identifiers(frag_rig, lookup_dict, skel_hierarchy)
        if found_object:
            object_list.append(found_object)

    if not object_list:
        return
    attach_dict['parent_object_list'] = object_list

    frag_parent_list = []
    for x in object_list:
        try:
            frag_node = frag.FRAGNode(lists.get_first_in_list(x.listConnections(type=pm.nt.Network)))
            frag_parent_list.append(frag_node)
        except:
            pass

    rig_component.attach_component(parent_component_list=frag_parent_list, **attach_dict)


def get_object_from_identifiers(frag_rig, identifier_dict, skel_hierarchy=None):
    """
    From a dictionary of identifiers find the object local to the given FRAG rig that matches them.

    :param FRAGRig frag_rig: The frag rig to use as the local lookup for the object.
    :param dict identifier_dict: A dictionary containing lookup identifiers for finding this object locally to the rig.
    :param ChainMarkup skel_hierarchy: The ChainMarkup representing the skeleton associated with the frag rig.
        By providing this it reduces the time to build. Otherwise, we'll derive it from the passed Joint.
    :return: The found object
    :rtype: Transform
    """

    object_type = identifier_dict.get('type')
    if object_type == 'flag':
        rig_component = lists.get_first_in_list(
            frag_rig.get_frag_children(side=identifier_dict.get('side'), region=identifier_dict.get('region')))
        flag_list = rig_component.get_flags()
        object_index = identifier_dict.get('index', 0)
        if flag_list:
            return flag_list[object_index] if len(flag_list) >= object_index else flag_list[0]
    elif object_type == 'skeleton':
        if not skel_hierarchy:
            frag_root = frag_rig.get_root()
            skel_root = frag_root.root_joint
            skel_hierarchy = chain_markup.ChainMarkup(skel_root)
        skel_chain = skel_hierarchy.get_full_chain(identifier_dict.get('region'), identifier_dict.get('side'))
        object_index = identifier_dict.get('index', 0)
        if skel_chain:
            return skel_chain[object_index] if len(skel_chain) >= object_index else skel_chain[0]
    elif object_type == 'named_object':
        return lists.get_first_in_list(pm.ls(identifier_dict.get('name')))


def get_serialized_rig_path(nodes):
    """
    Returns the FRAG Rig and the full path to where the rig build instructions should be saved.

    :param list(FRAGNodes) nodes: a list of FRAGNodes.
    :return: A list containing the FRAG Rig and the full path to where the rig build instructions should be saved.
    :rtype: list(FRAGRig, str)
    """

    if not isinstance(nodes, list):
        nodes = [nodes]

    frag_rig = None
    for selected_node in nodes:
        # find us a valid frag_rig
        frag_rig = frag.get_frag_rig(selected_node)
        if frag_rig:
            break

    if not frag_rig:
        return

    frag_root = frag_rig.get_root()
    asset_id = frag_root.asset_id
    mca_asset = assetlist.get_asset_by_id(asset_id)

    start_path = mca_asset.rigs_path if mca_asset else os.path.join(project_paths._PROJECT_ROOT, 'Characters')

    return [frag_rig, start_path]


def save_serialized_rig_cmd():
    """
    From selection find the FRAG Rig and serialize the build instructions for each component.

    """

    selection = pm.selected()
    frag_rig, start_path = get_serialized_rig_path(selection)

    found_path = dialogs.save_file_dialog(title='Select Rig', filters='MCARig (*.rig)', start_dir=start_path)
    if not found_path:
        return

    SerializeRig.save(frag_rig, found_path)


def load_serialized_rig_cmd():
    """
    From the given path read the build instructions for a rig and build them on the FRAG Rig.

    :param str rig_path: The full path to where the rig build instructions are.
    """

    selection = pm.selected()
    frag_rig, start_path = get_serialized_rig_path(selection)

    rig_path = dialogs.open_file_dialog(title='Select Rig', filters='MCARig (*.rig)', start_dir=start_path)
    if not rig_path:
        return

    rig_data = SerializeRig.load(frag_rig, rig_path)
    build_serialized_rig(frag_rig, rig_data.rig_build_list)


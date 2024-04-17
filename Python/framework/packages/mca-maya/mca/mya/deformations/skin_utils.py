#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that interact with Maya skinning
"""

# python imports
import os
# software specific imports
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as OpenMayaAnim
# mca python imports
from mca.common import log
from mca.common.paths import paths
from mca.common.textio import jsonio
from mca.common.utils import lists, fileio
from mca.common.tools.progressbar import progressbar_ui
from mca.mya.utils.om import om_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.utils import dag, naming, attr_utils, fbx_utils
from mca.mya.rigging import joint_utils, rig_utils, skel_utils
from mca.mya.animation import time_utils
from mca.mya.modeling import vert_utils
from mca.mya.pyqt import dialogs
from mca.mya.plugins.skinningConverter.python import skinningConverter

logger = log.MCA_LOGGER

DEFAULT_MAX_INFLUENCES = 4
_FIND_SKIN_SUPPORTED_SHAPE_TYPES = {'kMesh', 'kNurbsCurve', 'kNurbsSurface'}
_FIND_SKIN_SUPPORTED_COMPONENT_TYPES = {'kMeshVertComponent', 'kMeshPolygonComponent', 'kMeshEdgeComponent',
                                        'kSurfaceCVComponent', 'kCurveCVComponent'}


def get_skin_cluster_from_geometry(geo):
    """
    Returns the skinCluster node attached to the specified geometry transform/shape node.

    :param str/PyNode geo: geometry transform or shape node.
    :return: related skin cluster.
    :rtype: str or None
    """

    if not pm.objExists(geo):
        return None

    if isinstance(geo, pm.nt.Mesh):
        shape_node = geo
    else:
        shapes = geo.getShapes()
        shape_node = shapes[0] if shapes else None
    if not shape_node:
        return None

    skin_cluster = mel.eval('findRelatedSkinCluster("{}")'.format(shape_node.longName()))
    if not skin_cluster:
        skin_cluster = pm.ls(pm.listHistory(shape_node), type='skinCluster')
        if skin_cluster:
            skin_cluster = skin_cluster[0]
    if not skin_cluster:
        return None

    return skin_cluster


def get_influences(skinned_mesh, skip_namespace=False):
    """
    Returns all joint influences from the given skinned mesh.

    :param str or pm.PYNode skinned_mesh: mesh with a SkinCluster applied to it.
    :param bool skip_namespace: whether to remove namespace from influences.
    :return: list of influences of the skinned mesh.
    :rtype: list(pm.PyNode)
    """

    skin_cluster_name = get_skin_cluster_from_geometry(skinned_mesh)
    if not skin_cluster_name:
        return list()

    if skip_namespace:
        influences = [joint.split(':')[1] for joint in pm.skinCluster(skin_cluster_name, q=True, inf=True)]
    else:
        influences = pm.skinCluster(skin_cluster_name, q=True, inf=True)
    influences = list(set(influences))

    return influences


@ma_decorators.not_undoable_decorator
def find_related_skin_cluster(skin_obj):
    """
    Returns the skinCluster for a given bound object.

    :param PyNode skin_obj: Can be a Transform, Shape, Vertex/Edge/Face, or a CV component on a curve or surface.
    :return: Found skinCluster or None
    :rtype SkinCluster:
    """

    # don't work directly on a PyNode's internal variables as you can end up modifying the PyNode.
    source_mobj = om.MObject(skin_obj.__apimobject__())
    source_type = source_mobj.apiTypeStr()

    # determine a valid shape node from whatever object type we were given through the skin_obj arg
    if source_type in _FIND_SKIN_SUPPORTED_SHAPE_TYPES:
        shape_mobj = source_mobj
    elif source_type in _FIND_SKIN_SUPPORTED_COMPONENT_TYPES:
        # NOTE from docs: "Components do not contain any information about the surface that they refer to"
        source_mobj = om.MObject(skin_obj.__apimdagpath__().node())
        shape_type = source_mobj.apiTypeStr()
        if shape_type in _FIND_SKIN_SUPPORTED_SHAPE_TYPES:
            shape_mobj = source_mobj
        else:
            'Given shape type \'{0}\' is not supported.'.format(shape_type)
            return None

    elif source_type == 'kTransform':
        # be careful when running functions on internal pymel variables
        # if you directly use the PyObj's internal dag variable, there's a possibility you can modify the PyNode.
        source_dag = om.MDagPath(skin_obj.__apimdagpath__())
        # get the first shape under the transform.
        try:
            source_dag.extendToShapeDirectlyBelow(0)
            shape_mobj = source_dag.node()
            shape_type = shape_mobj.apiTypeStr()
            if shape_type not in _FIND_SKIN_SUPPORTED_SHAPE_TYPES:
                'Given shape type \'{0}\' is not supported.'.format(shape_type)
                return None
        except RuntimeError as exc:
            # OpenMaya raises a RuntimeError if there are 0 or 2+ shapes.
            'Given transform \'{0}\' either has multiple or zero shapes.'.format(skin_obj)
            return None
    else:
        'Given object type \'{0}\' is not supported.'.format(source_type)
        return None

    skin_cluster_mobj_list = []

    # Iterate up the shape node's dependency graph connections using a skinCluster-type filter
    it_dg = om.MItDependencyGraph(shape_mobj,
                                    om.MFn.kSkinClusterFilter,
                                    om.MItDependencyGraph.kUpstream,
                                    om.MItDependencyGraph.kDepthFirst,
                                    om.MItDependencyGraph.kNodeLevel)

    if it_dg.isDone():
        # since we are using a skinCluster filter, the iterator will initialize as "finished" if
        # it finds no skinClusters upstream to iterate over.
        'Given object \'{0}\' is not skinned.'.format(skin_obj)
        return None

    while not it_dg.isDone():
        # since we're filtering by kSkinClusterFilter, every item we iterate over will be of that type
        skin_cluster_mobj_list.append(it_dg.currentItem())
        it_dg.next()

    # take the first skin cluster we find. A shape node shouldn't have multiple skin clusters in its history.
    skin_cluster = lists.get_first_in_list([pm.PyNode(mobject) for mobject in skin_cluster_mobj_list])

    return skin_cluster


def copy_skin_weights(source_list, target_list, match_influences, max_influences=DEFAULT_MAX_INFLUENCES):
    """
    Copies skin weights between objects with option to force influences.

    :param list[pm.nt.Transform|pm.MeshVertex] source_list: A list of shaped Transforms, or MeshVerts that will be used as the source for the copy.
    :param list[pm.nt.Transform|pm.MeshVertex] target_list: A list of shaped Transforms, or MeshVerts that will be used at the target for the copy. These will receive influence values.
    :param bool match_influences: If all target mesh influence list should be updated to match the source influences.
    :param int max_influences: The maximum number of influences any new skin binds should have.
    :return: None or True if successful.
    :rtype Bool|None:
    """

    if (not source_list or not target_list) and source_list != target_list:
        # need to have both targets and sources.
        return
    filtered_source_list = []
    filtered_target_list = []
    match_skin_cluster_list = []
    for index, (original_list, filtered_list) in enumerate(
            [(source_list, filtered_source_list), (target_list, filtered_target_list)]):
        for x in original_list:
            for y in [x] + pm.listRelatives(x, ad=True, type=pm.nt.Transform):
                if (isinstance(y, pm.nt.Transform) and y.getShape() and y not in filtered_list)\
                            or (isinstance(y, list) and isinstance(y[0], pm.MeshVertex)):
                    # for each shaped transform, or list of meshverts
                    if not index:
                        # if we're running through the source list
                        skin_cluster_node = find_related_skin_cluster(y[0].node()) if isinstance(y, list)\
                                               and isinstance(y[0], pm.MeshVertex) else find_related_skin_cluster(y)
                        if not skin_cluster_node:
                            # s node can't be a source if it has no skinCluster
                            continue
                        match_skin_cluster_list.append(skin_cluster_node)
                    filtered_list.append(y)
    if not filtered_source_list or not filtered_target_list:
        # need to have object lists to operate on.
        return
    match_influence_list = []
    for x in match_skin_cluster_list:
        # collect a unique list of all potential influences.
        match_influence_list += pm.skinCluster(x, q=True, influence=True)
    list(set(match_influence_list))
    for target_node in filtered_target_list:
        base_node = target_node[0].node() if isinstance(target_node, list)\
                                             and isinstance(target_node[0], pm.MeshVertex) else target_node
        skin_cluster_node = find_related_skin_cluster(base_node)
        if not skin_cluster_node:
            try:
                skin_cluster_node = pm.skinCluster(base_node, match_influence_list, tsb=True,
                                                   normalizeWeights=1, maximumInfluences=max_influences,
                                                   obeyMaxInfluences=True, removeUnusedInfluence=False)
            except Exception as exc:
                continue
        if match_influences:
            current_influences = pm.skinCluster(skin_cluster_node, query=True, influence=True)
            pm.skinCluster(skin_cluster_node, edit=True,
                           addInfluence=[y for y in match_influence_list if y not in current_influences], weight=0)
        # selection just works better for the copySkinWeights function.
        pm.select(filtered_source_list + [target_node])
        pm.copySkinWeights(noMirror=True, sa='closestPoint', ia=['oneToOne', 'name', 'closestJoint'], normalize=True)
    return True


def get_all_hierarchy_bind_roots(node):
    """
    From a given node find all potential bind roots for that hierarchy.

    :param Transform node: A node within the hierarchy to traverse.
    :return: A list of all potential bind roots.
    :rtype: list[Joint]
    """

    bind_root_list = []
    parent_node = dag.get_absolute_parent(node)
    search_list = [parent_node] + pm.listRelatives(parent_node, ad=True, type=pm.nt.Transform)
    for node in search_list:
        if node and node.getShape():
            skin_cluster = find_related_skin_cluster(node)
            if skin_cluster:
                influence_list = skin_cluster.influenceObjects()
                if influence_list:
                    bind_root = dag.get_absolute_parent(influence_list[0], pm.nt.Joint)
                    if bind_root not in bind_root_list:
                        bind_root_list.append(bind_root)
    return bind_root_list


def rebind_mesh_to_skel(node_list, bind_root):
    """
    Rebind a mesh from one skeleton in the scene to another.

    :param list[Transform] node_list: A list of shaped transforms.
    :param Joint bind_root: The root of the skeleton we want to rebind the mesh to.
    """
    
    if not node_list:
        return

    original_influence_list = set()
    node_cluster_list = []
    for node in node_list:
        cluster = find_related_skin_cluster(node)
        if cluster:
            node_cluster_list.append([node, cluster])
            original_influence_list.update(set(cluster.getInfluence()))

    original_bind_names = [naming.get_basename(x) if not naming.get_basename(x).startswith('root') else 'root' for x in original_influence_list]
    target_skel_dict = joint_utils.create_skeleton_dict(bind_root)
    match_influence_list = []
    for joint_name in original_bind_names:
        target_influence = target_skel_dict.get(joint_name, None)
        if not target_influence:
            logger.error(f'Failed to find {joint_name} on the target skeleton')
            raise
        match_influence_list.append(target_influence)

    delete_me_group = pm.group(n='delete_me', em=True, w=True)
    for node, cluster in node_cluster_list:
        dupe = pm.duplicate(node)[0]
        dupe.setParent(delete_me_group)

        skin_cluster_node = pm.skinCluster(dupe, match_influence_list, tsb=True,
                                           normalizeWeights=1, maximumInfluences=4,
                                           obeyMaxInfluences=True, removeUnusedInfluence=False)
        pm.select(node, dupe)
        pm.copySkinWeights(noMirror=True, sa='closestPoint', ia=['oneToOne', 'name', 'closestJoint'], normalize=True)

        # we're doing a dance here so we don't lose the original passed objects,
        # just the new duplicates we're using to hold the skinning data.
        cluster.unbind()

        skin_cluster_node = pm.skinCluster(node, match_influence_list, tsb=True,
                                           normalizeWeights=1, maximumInfluences=4,
                                           obeyMaxInfluences=True, removeUnusedInfluence=False)
        pm.select(dupe, node)
        pm.copySkinWeights(noMirror=True, sa='closestPoint', ia=['oneToOne', 'name', 'closestJoint'], normalize=True)
    pm.delete(delete_me_group)

    """
    # this is crap performance. it does use open mya to run but it's just too slow.
    source_weight_dict = get_open_maya_skin_weight_assignment(node)
    if not source_weight_dict:
        logger.warning('Unable to get weight_dict')
        return
    # get original skel dict
    skel_hierarchy = joint.create_skeleton_dict(dag_utils.get_absolute_parent(list(source_weight_dict.keys())[0]))
    # invert values for remapping
    skel_hierarchy = {v: k for k, v in skel_hierarchy.items()}

    remap_skel_hierarchy = joint.create_skeleton_dict(bind_root)
    remap_dict = {}
    for joint_node, data_list in source_weight_dict.items():
        joint_name = skel_hierarchy.get(joint_node, None)
        if joint_name in remap_skel_hierarchy:
            remap_dict[remap_skel_hierarchy[joint_name]] = data_list
        else:
            raise f'{joint_name} Missing influence could not be found in the target skeleton.'
    skin_cluster = find_related_skin_cluster(node)
    skin_cluster.unbind()
    open_maya_skin_weight_assignment(node, remap_dict)joint_utils
    """


def skinning_converter_cmd(joints, start_frame, end_frame, meshes=None):
    """
    Runs the Hans Godard Linear Skinning Decomposition Plugin.

    :param list(str) joints: List of joints that get skinned
    :param int start_frame: Start frame of the poses
    :param int end_frame: End frame of the poses
    :param list(str) end_frame: End frame of the poses
    :param list(str) meshes: List of meshes to get skinned.
    :return: Returns a dictionary of everything that was created.
    :rtype: Dictionary
    """
    
    if not meshes:
        meshes = skinningConverter.get_selected_meshes()
    
    existingJoints = joints
    numJoint = len(existingJoints)
    makeRoot = None
    maxIteration = 1  # no joint iteration
    
    maxInf = 4
    
    # endFrame is included
    startFrame = int(start_frame)
    endFrame = int(end_frame)
    
    if startFrame >= endFrame:
        cmds.warning('startFrame must be < endFrame')
        return
    
    frames = [float(item) for item in range(startFrame, endFrame + 1)]
    
    if len(frames) < 2:
        cmds.warning('Need at least 2 frames ( here frames are %s )' % frames)
        return
    
    # doit
    errorPercentBreak = 1.0  # usused if -1.0
    rigidMatrices = True
    
    cmds.undoInfo(openChunk=True)
    cmds.refresh(suspend=True)
    result = skinningConverter.from_scratch(meshes,
                                            existingJoints,
                                            numJoint,
                                            maxInf,
                                            frames,
                                            maxIteration,
                                            errorPercentBreak=errorPercentBreak,
                                            deleteInitJoints=True,
                                            rigidMatrices=rigidMatrices,
                                            makeRoot=makeRoot, )
    cmds.refresh(suspend=False)
    cmds.undoInfo(closeChunk=True)
    
    return result

@ma_decorators.undo_decorator
@ma_decorators.keep_selection_decorator
def swap_vertex_influence_weight_cmd():
    """
    Takes all the influence of the first joint and replaces it with the second selected joint to all selected vertices.

    """

    vertex_operators = pm.filterExpand(pm.selected(), sm=31)
    selected_joints = pm.ls(sl=True, type=pm.nt.Joint)

    if vertex_operators:
        mesh_skin_cluster = find_related_skin_cluster(pm.PyNode(vertex_operators[0]).node().getParent())
    else:
        'Selection Error: Select one or more vertices'
        return

    if selected_joints and selected_joints[0] != selected_joints[-1]:
        source_joint_list = selected_joints[:-1]
        destination_joint = selected_joints[-1]
    else:
        'Selection Error: Select two different joints to swap influences.'
        return
    for source_joint in source_joint_list:
        for x in vertex_operators:
            src_value = pm.skinPercent(mesh_skin_cluster, x, q=True, transform=source_joint, v=True)  # collect source influence.
            set_value = pm.skinPercent(mesh_skin_cluster, x, q=True, transform=destination_joint, v=True) + src_value  # collect destination influence
            pm.skinPercent(mesh_skin_cluster, x, transformValue=[(source_joint, 0), (destination_joint, set_value)])  # set source to 0 Set destination to combined value.


def set_skin_weights(weight_dictionary, blend_weights, shape_node, influence_set=None, dual_quat=False):
    """
    Unlocks all transform values on the given transform node.

    :param dict weight_dictionary: Dict with joints as keys and lists of influence values sorted by vertex ID as values
    :param list(float) blend_weights: list of blend weights containing influence values on vertices
    :param str or pm.nt.Transform shape_node: Mesh to apply skinning to
    :param list[str] influence_set: List of joint names including all that were previously saved in the old skinCluster
    :param bool dual_quat: Skinning method, False uses classic linear and True uses dual quaternion
    """

    selection_list = om.MSelectionList()
    shape_node = pm.PyNode(shape_node)
    shape_node.visibility.set(1)
    paths = om.MDagPathArray()
    script_util = om.MScriptUtil()
    influence_index_array = om.MIntArray()
    influence_value_array = om.MDoubleArray()
    blend_weights_da = om.MDoubleArray()
    for bw in blend_weights:
        blend_weights_da.append(bw)
    # create a node to id cache
    node_to_id = {}
    missing_bones = []
    for bone_id in weight_dictionary:
        if bone_id in influence_set:
            node_to_id[pm.PyNode(bone_id)] = bone_id
        else:
            missing_bones.append(bone_id)

    # if there are no bones from the skin in the scene, then we're done
    if not node_to_id:
        logger.warning('Missing all joints needed for skinning')
        return

    # delete existing skin clusters for this mesh
    skin_cluster = find_related_skin_cluster(shape_node)
    if skin_cluster:
        skin_cluster.unbind()

    attr_utils.unlock_all_attrs(shape_node)
    # Need toSelectedBones=True, otherwise Maya may bind every joint in the skeleton, resulting in a huge perf hit when removing unused influences
    pm.select(cl=1)  # Selected objects potentially cause issues when calling skinCluster with toSelectedBones=True
    skin_cluster = pm.skinCluster([node for node in node_to_id], shape_node, skinMethod=(1 if dual_quat else 0),
                                  maximumInfluences=4, obeyMaxInfluences=True, toSelectedBones=True)
    pm.select(cl=1)  # Maya will have auto-selected joints so clear selection again
    selection_list.add(skin_cluster.name())
    skin_cluster_depend_node = om.MObject()
    selection_list.getDependNode(0, skin_cluster_depend_node)
    fn_skin_cluster = OpenMayaAnim.MFnSkinCluster(skin_cluster_depend_node)
    fn_skin_cluster.influenceObjects(paths)

    influence_index_to_id = []
    for i in range(0, paths.length()):
        path_node = pm.PyNode(paths[i])
        influence_index_array.append(fn_skin_cluster.indexForInfluenceObject(paths[i]))

        if path_node in node_to_id.keys():
            influence_index_to_id.append(node_to_id[path_node])
        else:
            influence_index_to_id.append(None)

    selection_list.clear()
    selection_list.add(shape_node.fullPath() + ".f[:]")
    dag_path = om.MDagPath()
    face_component = om.MObject()
    selection_list.getDagPath(0, dag_path, face_component)

    selection_list.clear()
    selection_list.add(shape_node.fullPath() + ".vtx[:]")
    vert_component = om.MObject()
    selection_list.getDagPath(0, dag_path, vert_component)
    fn_vert_component = om.MFnComponent(vert_component)

    # Create an array of vertices * joints size and fill with the weight values
    for vert_index in range(0, fn_vert_component.elementCount()):
        for influence_index, vert_id in enumerate(influence_index_to_id):
            if vert_id:
                influence_value_array.append(weight_dictionary[vert_id][vert_index])
            else:
                influence_value_array.append(0.0)

    fn_skin_cluster.setWeights(dag_path, face_component, influence_index_array, influence_value_array, False)
    fn_skin_cluster.setBlendWeights(dag_path, face_component, blend_weights_da)

    # Remove any remaining unused influences
    influences = skin_cluster.getInfluence()
    weighted_influences = set(skin_cluster.getWeightedInfluence())
    remove_influence_list = list(filter(lambda inf: not (inf in weighted_influences), influences))
    skin_cluster.removeInfluence(remove_influence_list)
    if missing_bones:
        # Missing bones will cause anything with their influence to have weights that do not equal 1.0, normalizing here
        pm.skinPercent(skin_cluster, shape_node, nrm=True)
        list(map(lambda x: logger.warning(f'Missing joint: {x} from saved weights'), missing_bones))


def get_skin_weights(mesh_node):
    """
    Gets skin weight data from a mesh and returns it as a dict for skin weights and list for blend weights
    :param pm.nt.Transform mesh_node: The mesh we want to get skinning data from
    :return: Dictionary with vertex IDs as keys and lists of tuples as values [(joint name, influence value)] and a
    list of blend weights with influence values on vertices
    :rtype: dict, list

    """

    if not isinstance(mesh_node, pm.PyNode):
        mesh_node = pm.PyNode(mesh_node)

    skin_cluster = find_related_skin_cluster(mesh_node)

    if not skin_cluster:
        logger.warning(f'{mesh_node} is not skinned')
        return {}, []

    weight_dictionary = {}
    paths = om.MDagPathArray()
    influence_indices = om.MIntArray()

    # Access the api fn set for the skin cluster
    fn_skin_cluster = skin_cluster.__apimfn__()

    # Get a MDagPathList of MDagPath objects, which are the skin cluster's influences.
    fn_skin_cluster.influenceObjects(paths)
    num_influences = paths.length()
    bone_ids = []

    for i in range(0, num_influences):
        influence_indices.append(i)
        joint = pm.PyNode(paths[i].node())
        bone_ids.append(naming.get_basename(joint))

    selection_list = om.MSelectionList()
    # getBlendWeights needs a component of the same size
    selection_list.add(mesh_node.name() + '.vtx[:]')
    components = om.MObject()
    geometry_path = om.MDagPath()
    selection_list.getDagPath(0, geometry_path, components)

    weights = om.MDoubleArray()
    # dual quaternion blending weights for this mesh
    blend_weights = om.MDoubleArray()

    # Get weights once
    fn_skin_cluster.getWeights(geometry_path, components, influence_indices, weights)
    fn_skin_cluster.getBlendWeights(geometry_path, components, blend_weights)

    # Keep consistent return types
    weights = list(weights)
    blend_weights = list(blend_weights)
    # Create a double array that represents an influence with 0.0 for all of its weights.
    null_weight_list = [0.0] * num_influences
    # This logic essentially just gives a weight to _something_. We don't necessarily know
    # what the influence at that final index will be.
    default_weight_list = [0.0] * (num_influences - 1)
    default_weight_list.append(1.0)

    # Check for vertices with 0 weights. We don't necessarily have to set up a geometry iterator for this
    # since we don't need any information from it besides an index.

    for vertex_index in range(0, mesh_node.numVertices()):
        vertex_weight_slice_start = vertex_index * num_influences
        vertex_weights = weights[vertex_weight_slice_start: vertex_weight_slice_start + num_influences]

        if vertex_weights == null_weight_list:
            weights[vertex_weight_slice_start: vertex_weight_slice_start + num_influences] = default_weight_list

    # Fill the weight dictionary by taking column slices of the weight matrix
    for i in range(0, num_influences):
        # The current influence's weights is column i of the weight matrix
        influence_weights = weights[i:: num_influences]
        weight_dictionary[bone_ids[i]] = influence_weights

    return weight_dictionary, blend_weights


def get_vert_weights_from_skin_data(weight_data):
    """
    Converts weight data dict to a format we can easily use with PyMel commands

    :param dict weight_data: Dict with joint names as keys and lists of influence values sorted by vertex ID as values
    :return: Weight dictionary with vertex IDs as keys and lists of tuples as values [(joint name: influence value)]
    :rtype: dict
    """

    weight_map = {}

    for jnt in weight_data.keys():
        num_verts = len(weight_data.get(jnt))
        for vert_id in range(num_verts):
            weight_map[vert_id] = []
            for bone_id in weight_data.keys():
                bone_weight = weight_data[bone_id][vert_id]
                if bone_weight:
                    if isinstance(bone_id, pm.nt.Joint):
                        bone_id = bone_id.name()
                    weight_map[vert_id].append((bone_id, bone_weight))
    return weight_map


def get_weight_data_from_vert_weights(vert_weights):
    """
    Converts vertex weight data from {vertex id: [(joint1, weight value),(joint2, weight value)]} to structure
    used by set_skin_weights(): {joint1: [wv, wv, wv, wv, ...], joint2: [wv, wv, wv, wv, ...]} with weight
    values being in corresponding order with the vertex ID

    :param dict vert_weights: Vertex weight dictionary to rearrange
    :return: Returns a dictionary of skin weights
    :rtype: dict
    """

    weight_data = {}
    num_vertices = len(vert_weights.keys())
    # get all bone influences
    influence_bones = set()
    for bone_list in vert_weights.values():
        for bone_id, bone_weight in bone_list:
            if isinstance(bone_id, pm.nt.Joint):
                bone_id = bone_id.name()
            influence_bones.add(bone_id)
    # setup weight table
    for bone in influence_bones:
        weight_data[bone] = [0] * num_vertices
    # fill out weight table
    for vert_id, bone_list in vert_weights.items():
        for bone_id, bone_weight in bone_list:
            weight_data[bone_id][vert_id] = bone_weight
    return weight_data


def set_vertex_weights(vert_ids, mesh_name, weight_map):
    """
    Sets previously saved vertex weights onto a mesh with the same vert count

    :param list(int) vert_ids: A list of vertex IDs to apply skinning to
    :param str mesh_name: Name of the mesh that the vertices belong to
    :param dict weight_map: Dict with vertex IDs as keys and lists of tuples [(joint name, influence value)] as values
    :return: True if weights were applied, else False
    :rtype: bool
    """

    if isinstance(vert_ids, (int, float)):
    # Recast as a list with an integar rather than a float or just int.
        vert_ids = [int(vert_ids)]
    if not vert_ids:
        return False

    skin_cluster = find_related_skin_cluster(pm.PyNode(mesh_name))
    if not skin_cluster:
        return False
    # Get all influences for the skin cluster
    influence_objects = list(map(lambda x: x.name(), skin_cluster.getInfluence()))
    # Get all joints that were weighted in the saved skin data file
    weight_map_jnts = list(set(x[0] for y in weight_map.values() for x in y))
    # Figure out if any saved influences are missing from the cluster, add them if any are found
    missing_from_clus = [x for x in weight_map_jnts if x not in influence_objects]
    if missing_from_clus:
        missing_jnts = [x for x in missing_from_clus if not pm.objExists(x)]
        if missing_jnts:
            logger.warning(f'Missing joints needed to apply skinning: {missing_jnts}')
            return False
        else:
            logger.warning(f'Adding joints to {mesh_name} skin clus: {missing_from_clus}')
            skin_cluster.addInfluence(missing_from_clus, wt=0)
    for vert_id in vert_ids:
        if vert_id not in weight_map:
            continue

        pm.skinPercent(skin_cluster, f'{mesh_name}.vtx[{vert_id}]', tv=weight_map[vert_id])
    return True


def apply_skin_weights_cmd(skin_data_path):
    """
    Applies previously saved skin weights to selected meshes or vertices

    :param str skin_data_path: Path to skin data folder to pull weight data file from
    """

    selected_nodes = pm.selected(fl=True)
    first_node = lists.get_first_in_list(selected_nodes)
    if not first_node:
        logger.warning('Please select meshes or vertices to apply skinning to')
        return
    first_type = type(first_node)
    is_same_type = all(isinstance(item, first_type) for item in selected_nodes)
    if not is_same_type and (isinstance(first_node, pm.MeshVertex)
                         or isinstance(first_node, pm.nt.Transform)):
        logger.warning('Please select either vertices or meshes to apply weights on')
        return

    if first_type == pm.MeshVertex:
        # In case vertices from multiple meshes are selected, separating them by mesh here
        apply_skinning_to_verts(selected_nodes, skin_data_path)

    else:
        apply_skinning_to_mesh(selected_nodes, skin_data_path)


def save_skin_weights_cmd(skin_data_path):
    """
    Saves selected meshes skin weights

    :param str skin_data_path: Path to skin data folder where we want to place weight data file
    """

    selected_nodes = pm.selected()
    if not selected_nodes:
        logger.warning('Please select meshes to save skinning from')
        return

    for node in selected_nodes:
        if isinstance(node, pm.nt.Transform):
            skin_data = get_skin_weights(node)
            skin_data_file = os.path.join(skin_data_path, f'{node.name()}_skin_data.json')
            if os.path.exists(skin_data_file):
                fileio.touch_path(skin_data_path)
            jsonio.write_to_json_file(skin_data, skin_data_file)

def apply_skinning_to_verts(vertex_list, skin_data_path, name_override=''):
    """
    Applies previously saved skin weights to vertices

    :param list(pm.MeshVertex) vertex_list: List of vertices to apply skinning to
    :param str skin_data_path: Path to skin data folder to pull weight data file from
    :param str name_override: Name of data to look for if different from mesh name
    """

    # In case vertices from multiple meshes are selected, separating them by mesh here
    meshes_ids = {}
    for node in vertex_list:
        mesh_name = node.node().getParent().name()
        if mesh_name not in meshes_ids:
            meshes_ids[mesh_name] = []
        vert_id = node.index()
        meshes_ids[mesh_name].append(vert_id)

    for mesh, ids in meshes_ids.items():
        if name_override == '':
            data_name = mesh
        else:
            data_name = name_override

        if not os.path.exists(os.path.join(skin_data_path, f'{data_name}_skin_data.json')):
            logger.warning(f'Could not find skin data file for {mesh}')
            continue

        weight_data = jsonio.read_json_file(os.path.join(skin_data_path, f'{data_name}_skin_data.json'))[0]
        if not weight_data:
            logger.warning(f'Weight data not found for {mesh}')
            continue

        weight_dict = get_vert_weights_from_skin_data(weight_data)
        set_vertex_weights(ids, mesh, weight_dict)


def apply_skinning_to_mesh(mesh_list, skin_data_path, name_override=''):
    """
    Applies previously saved skin weights to selected meshes or vertices

    :param list(pm.nt.Transform) mesh_list: List of meshes to apply skinning to
    :param str skin_data_path: Path to skin data folder to pull weight data file from
    :param str name_override: Name to look for in skin data file
    """

    for node in mesh_list:
        if isinstance(node, str):
            node = pm.PyNode(node)
        if isinstance(node, pm.nt.Transform):
            if name_override == '':
                node_name = node.name()
            else:
                node_name = name_override
            if not os.path.exists(os.path.join(skin_data_path, f'{node_name}_skin_data.json')):
                logger.warning(f'Could not find skin data file for {node_name}')
                continue
            weight_dict = jsonio.read_json_file(os.path.join(skin_data_path, f'{node_name}_skin_data.json'))
            # Since we are only going to actually add joints that were previously in the skin cluster to the new one
            # when adding influence, just grabbing all joints in scene as potential influences
            influ_set = list(map(lambda x: x.name(), pm.ls(type=pm.nt.Joint)))
            set_skin_weights(weight_dict[0], weight_dict[1], node, influence_set=influ_set)


def remove_wrong_side_influ(mesh_name,
                            right_vert_index_list,
                            left_vert_index_list,
                            joint_list,
                            l_r_labels=None,
                            prefix=True):
    """
    Removes left side joint influences from right side and vice versa.

    :param str mesh_name: Name of the mesh to operate on
    :param list(int) right_vert_index_list: List of vertex indices on the right side of mesh
    :param list(int) left_vert_index_list: List of vertex indices on the left side of mesh
    :param list(str) joint_list: List of joint names
    :param list(str) l_r_labels: Left and right joint name labels in that order
    :return: Returns weight dictionary and blend weights
    :rtype: dict, list
    """

    if not l_r_labels:
        l_r_labels = ['r_', 'l_']

    # Get weight dict
    weight_dictionary, blend_wghts = get_skin_weights(pm.PyNode(mesh_name))

    for vert_side_list, remove_side_label in zip([right_vert_index_list, left_vert_index_list], l_r_labels):
        # Get joints that are part of the side we are removing
        if prefix:
            jnts_to_set_zero_influ = [x for x in joint_list if remove_side_label in x and x[0] == remove_side_label[0]]
        else:
            jnts_to_set_zero_influ = [x for x in joint_list if
                                      remove_side_label in x and x[-1] == remove_side_label[-1]]

        for jnt in jnts_to_set_zero_influ:
            vert_influs = weight_dictionary.get(jnt)
            if vert_influs is not None:
                for x, vert in enumerate(vert_influs):
                    # Replace wrong side joint weight with the closest joint instead
                    if x in vert_side_list and vert != 0.0:
                        closest_joint = om_utils.get_closest_joint_to_vertex(x,
                                                                             mesh_name,
                                                                             [x for x in joint_list if '_null' not in x])
                        closest_joint_weights = weight_dictionary.get(closest_joint)
                        if closest_joint_weights:
                            vert_influs[x] = 0.0
                            closest_joint_weight = closest_joint_weights[x]
                            new_weight = vert + closest_joint_weight
                            if new_weight > 1.0:
                                new_weight = 1.0
                            closest_joint_weights[x] = new_weight

    return weight_dictionary, blend_wghts


def remove_keywords_influ_from_verts(mesh_name,
                                    vert_index_list,
                                    joint_list,
                                    keywords):
    """
    Removes influences from joints with a specific keyword in their name from a list of vertices.

    :param str mesh_name: Name of the mesh to operate on.
    :param list(int) vert_index_list: List of vertex indices on the mesh to operate on
    :param list(str) joint_list: List of joint names including all in skinCluster
    :param list(str) keywords: Keywords to look for in joint names to remove influence from
    """

    weight_dictionary, blend_wghts = get_skin_weights(pm.PyNode(mesh_name))

    for keyword in keywords:
        jnts_to_set_zero_influ = [x for x in joint_list if keyword in x]
        for jnt in jnts_to_set_zero_influ:
            vert_influs = weight_dictionary.get(jnt)
            if vert_influs is not None:
                for x, vert in enumerate(vert_influs):
                    if x in vert_index_list and vert != 0.0:
                        closest_joint = om_utils.get_closest_joint_to_vertex(x, mesh_name,
                                                                             [x for x in joint_list if
                                                                              '_null' not in x and
                                                                              keyword not in x])
                        closest_joint_weights = weight_dictionary.get(closest_joint)
                        if closest_joint_weights:
                            vert_influs[x] = 0.0
                            closest_joint_weight = closest_joint_weights[x]
                            new_weight = vert + closest_joint_weight
                            if new_weight > 1.0:
                                new_weight = 1.0
                            closest_joint_weights[x] = new_weight

    return weight_dictionary, blend_wghts


@ma_decorators.undo_decorator
def smooth_vertex_weight(vertex):
    """
    :param pm.nt.MeshVertex vertex: Vertex whose weights we want to smooth out.
    """
    shape_node = vertex.node()
    adjacent_vertices = vertex.connectedVertices()
    skin_cluster = get_skin_cluster_from_geometry(shape_node)
    skin_cluster = pm.PyNode(skin_cluster)
    added_weights = [0] * skin_cluster.numInfluenceObjects()
    for weights in skin_cluster.getWeights(adjacent_vertices):
        added_weights = map(sum, zip(weights, added_weights))
    top_4_weights = sorted(zip(skin_cluster.getInfluence(), added_weights), key=lambda x: x[1], reverse=True)[:4]
    pm.skinPercent(skin_cluster, vertex, transformValue=top_4_weights, normalize=True)


def smooth_mesh_weights(mesh):
    """
    Smooths out weights on a mesh

    :param pm.nt.Transform mesh: Mesh to smooth skin weights on
    """
    # Get skin data dict
    skin_data = get_skin_weights(mesh)
    influ_set = get_influences(mesh)
    # Convert dict
    skin_weights = get_vert_weights_from_skin_data(skin_data[0])
    vertices = pm.ls(f'{mesh.getShape()}.vtx[*]', fl=True)
    skin_cluster = get_skin_cluster_from_geometry(mesh)
    skin_cluster = pm.PyNode(skin_cluster)

    for vertex in vertices:
        vertex_id = vertex.index()
        adjacent_vertices = vertex.connectedVertices()

        # Initialize a list for weights
        added_weights = [0] * skin_cluster.numInfluenceObjects()
        for weights in skin_cluster.getWeights(adjacent_vertices):
            added_weights = map(sum, zip(weights, added_weights))
        # Sort weights by highest value
        top_4_weights = sorted(zip(skin_cluster.getInfluence(), added_weights), key=lambda x: x[1], reverse=True)[:4]

        jnt_list, weights_list = [list(t) for t in zip(*top_4_weights)]
        joints_list = []
        for jnt in jnt_list:
            if isinstance(jnt, pm.nt.Joint):
                jnt = jnt.name()
            joints_list.append(jnt)

        # Normalize weights
        normalized_weights = [num / sum(weights_list) for num in weights_list]
        new_weights = list(zip(joints_list, normalized_weights))
        skin_weights[vertex_id] = new_weights

    skin_data_new = get_weight_data_from_vert_weights(skin_weights)
    set_skin_weights(skin_data_new, skin_data[1], mesh, influence_set=[x.name() for x in influ_set])


def import_skin_wrap_mesh(archetype, deformed_mesh):
    """
    Creates a wrap deformer

    :param str archetype: Archetype for this mesh
    :param pm.nt.Transform deformed_mesh: The mesh to be deformed by the wrap deformer.
    :return: Returns the wrap node that was created and imported groups.
    :rtype: list(pm.nt.Wrap, pm.nt.Transform)
    """
    # Find, import, and skin wrap mesh
    wrap_meshes_path = os.path.join(paths.get_common_skinning(), f'WrapMeshes\{archetype}_wrap.fbx')
    if not os.path.exists(wrap_meshes_path):
        logger.warning(f'Could not find {wrap_meshes_path}')
        return
    imported_nodes = fbx_utils.import_fbx(wrap_meshes_path)
    wrap_mesh = [x for x in imported_nodes if isinstance(x, pm.nt.Transform)]
    if not wrap_mesh:
        return
    wrap_skin_data_path = os.path.join(paths.get_common_skinning(), f'WrapSkinData')
    apply_skinning_to_mesh(wrap_mesh, wrap_skin_data_path)

    # Meshes must be selected to use the CreateWrap command
    pm.select(deformed_mesh, r=True)
    pm.select(wrap_mesh, add=True)
    cmds.CreateWrap(deformed_mesh, wrap_mesh)

    # CreateWrap is a runtime command and returns nothing so finding the created wrap node here
    wrap_node = list(set(pm.listConnections(f'{deformed_mesh}Shape', type="wrap")))[0]
    wrap_node.rename('MCASkinningWrap')

    return [wrap_node, wrap_mesh[0]]


def auto_skin(archetype, main_mesh):
    """
    Skins a mesh based on archetype

    :param str archetype: Archetype for this mesh (used to find both skeleton and deformer mesh file)
    :param pm.nt.Transform main_mesh: Mesh to skin
    """
    prog_ui = progressbar_ui.ProgressBarStandard()
    prog_ui.update_status(0, 'Starting Up')
    prog_ui.update_status(5, f'Checking for skeleton...')
    # Check for bind root
    root_joint = get_all_hierarchy_bind_roots(main_mesh)
    if not root_joint:
        if pm.objExists('root'):
            root_joint = pm.PyNode('root')
        else:
            prog_ui.update_status(10, f'Importing {archetype} skeleton...')
            # If no root in scene import from archetype source
            skel_path = rig_utils.get_asset_skeleton(archetype)
            root_joint = skel_utils.import_skeleton(skel_path)
    prog_ui.update_status(15, f'Setting up wrap on {main_mesh}...')
    # Duplicate mesh, this will act like a blend shape
    dup_mesh = pm.duplicate(main_mesh)[0]
    # Set up wrap
    wrap_items = import_skin_wrap_mesh(archetype, dup_mesh)
    if not wrap_items:
        return
    wrap_node, wrap_mesh = wrap_items

    skin_joints = get_influences(wrap_mesh)
    if not skin_joints:
        pm.delete(wrap_mesh)
        prog_ui.update_status(100, f'Aborted operation on {main_mesh}')
        logger.warning('Issue with skinning wrap mesh')
        return

    # Apply animation for LSD to work
    pm.currentTime(0)
    list(map(lambda x: pm.setKeyframe(x, at='tx', t=0), skin_joints))
    for jnt in skin_joints:
        current_time = pm.currentTime(q=True)
        tx_val = jnt.tx.get()
        pm.setKeyframe(jnt, at='tx', v=tx_val, t=current_time)
        pm.setKeyframe(jnt, at='rz', v=0, t=current_time)
        pm.setKeyframe(jnt, at='rz', v=75, t=current_time + 1)
        pm.setKeyframe(jnt, at='rz', v=-75, t=current_time + 2)
        pm.setKeyframe(jnt, at='tx', v=30, t=current_time + 2)
        pm.setKeyframe(jnt, at='rz', v=0, t=current_time + 3)
        pm.setKeyframe(jnt, at='tx', v=tx_val, t=current_time + 3)
        pm.currentTime(current_time + 4)

    # Run skinning converter command
    prog_ui.update_status(30, f'Skinning {main_mesh}...')
    first_key, second_key = time_utils.get_times(skin_joints)
    run_skinning_converter_cmd(dup_mesh.name(), main_mesh.name(), skin_joints, first_key, second_key)

    # Cleanup
    pm.setCurrentTime(0)
    pm.delete(pm.ls(type=pm.nt.AnimCurve))
    list(map(lambda x: pm.PyNode(x).rz.set(0), skin_joints))
    pm.delete([dup_mesh, wrap_mesh])
    if isinstance(root_joint, list):
        root_joint = root_joint[0]

    # Meshes with too high of a poly count will cause ram to quickly exceed 32 GB when baking deformer
    num_vertices = main_mesh.numVertices()
    if num_vertices < 20000:
        prog_ui.update_status(60, f'Creating delta mush deformer on {main_mesh}...')
        delta_mush_node = pm.deltaMush(main_mesh, si=15, n='MCADeltaMush')
        prog_ui.update_status(80, f'Baking deformer on {main_mesh}...')
        pm.bakeDeformer(ss=root_joint, sm=main_mesh, ds=root_joint, dm=main_mesh, mi=4)
        pm.flushUndo()

    elif num_vertices < 60000:
        prog_ui.update_status(70, f'Smoothing weights on {main_mesh}...')
        smooth_mesh_weights(main_mesh)

    prog_ui.update_status(100, f'Finished!')


def run_skinning_converter_cmd(blendshape_mesh, skin_mesh, joints, start_frame, end_frame, delete_decomp_mesh=True):
    """
    Runs the Hans Godard Linear Skinning Decomposition Plugin.

    :param str/pm.nt.Transform blendshape_mesh: mesh to get skinned
    :param str/pm.nt.Transform skin_mesh: mesh to get skinned
    :param list(str/pm.nt.Joint) joints: List of joints that get skinned
    :param int start_frame: Start frame of the poses
    :param int end_frame: End frame of the poses
    :param list(str) end_frame: End frame of the poses
    :param bool delete_decomp_mesh: Deletes mesh duplicated for LSD process if True
    """

    pm.select(blendshape_mesh, joints)
    str_joints = cmds.ls(sl=True, type='joint')

    # run skinning tool!
    result = skinning_converter_cmd(str_joints, start_frame, end_frame)
    decomp_grp = result.get('meshGrp', None)
    if not decomp_grp:
        return

    decomp_mesh = lists.get_first_in_list(cmds.listRelatives(decomp_grp, c=True))
    if not decomp_mesh:
        return

    copy_skin_weights(source_list=[pm.PyNode(decomp_mesh)],
                      target_list=[pm.PyNode(skin_mesh)],
                      match_influences=True)
    if delete_decomp_mesh:
        pm.delete(result['meshGrp'])
    pm.select(cl=True)

    return


def get_mirrored_weights(mesh, vertex_list):
    if not vertex_list:
        return
    pymel_vert = pm.PyNode(vertex_list[0])
    source_skin_cluster = find_related_skin_cluster(pymel_vert.node().getParent())
    vertices = {}
    vertices['skinCluster'] = str(source_skin_cluster)

    for vert in vertex_list:
        opposite_vert = vert_utils.get_opposite_vertices([vert])
        opposite_vert = str(mesh) + '.vtx' + str(opposite_vert)
        vertices[opposite_vert] = {}
        joints = pm.skinPercent(source_skin_cluster, vert, transform=None, query=True)
        inf_joints = []
        for joint in joints:
            skin_weight = pm.skinPercent(source_skin_cluster, vert, transform=joint, query=True)
            if skin_weight > 0.0:
                inf_joints.append((joint, skin_weight))
        for joint, skin_weight in inf_joints:
            if '_l' in str(joint):
                vertices[opposite_vert][joint.replace('_l', '_r')] = skin_weight
            elif '_r' in str(joint):
                vertices[opposite_vert][joint.replace('_r', '_l')] = skin_weight
            else:
                vertices[opposite_vert][joint] = skin_weight
    return vertices


def mirror_vertex_weight(main_joint, vertices_list):
    # get the mesh
    mesh = str(pm.ls(vertices_list[0], o=True)[0].getParent())
    # get a dictionary with the opposite verts and opposite joints
    mirrored_weights = get_mirrored_weights(mesh, vertices_list)

    # get the skin cluster from the dictionary
    skin_cluster = mirrored_weights['skinCluster']

    # get all the influence joints and unlock them all
    inf_joints = cmds.skinCluster(skin_cluster, query=True, inf=True)
    for inf_joint in inf_joints:
        cmds.skinCluster(skin_cluster, inf=inf_joint, e=True, lw=False)

    for vert, weights in mirrored_weights.items():
        joints = []
        joint_list = []
        if vert != 'skinCluster':
            # transfer all the weight to the main joint
            cmds.skinPercent(skin_cluster, vert, transformValue=[(str(main_joint), 1.0)])
            # get the joint and weight info
            for joint, weight in weights.items():
                joints.append(str(joint))
                joint_list.append((str(joint), float(weight)))
            # lock all the weights except for the main joint and the influences that need added.
            for inf_joint in inf_joints:
                if str(main_joint) not in inf_joint and inf_joint not in joints:
                    cmds.skinCluster(skin_cluster, inf=inf_joint, e=True, lw=True)
            # Set the influences
            cmds.skinPercent(skin_cluster, vert, transformValue=joint_list)
            # unlock all the joints again.
            for inf_joint in inf_joints:
                cmds.skinCluster(skin_cluster, inf=inf_joint, e=True, lw=False)

    return


def mirror_vertex_weights_cmd(skip_dialog=False):
    if not skip_dialog:
        result = pm.confirmDialog(title='Mirror Vertex Weights',
                                  message='Mirror Selected Vertex Weights?\n',
                                  button=['Yes', 'No'],
                                  defaultButton='Yes',
                                  cancelButton='No',
                                  dismissString='No')
        if not result == 'Yes':
            return

    vertices_list = pm.selected(fl=True)
    vertices_list = [x for x in vertices_list if isinstance(x, pm.nt.general.MeshVertex)]
    if not vertices_list:
        return
    source_skin_cluster = find_related_skin_cluster(vertices_list[0].node().getParent())
    cluster_joints = pm.skinCluster(source_skin_cluster, q=True, wi=True)
    root_joint = dag.get_absolute_parent(cluster_joints[0], node_type=pm.nt.Joint)
    children_joints = dag.get_children_in_order(root_joint, pm.nt.Joint)
    main_joint = None
    for joint in children_joints:
        if joint in cluster_joints:
            main_joint = joint
            break
    if main_joint:
        mirror_vertex_weight(main_joint, vertices_list)

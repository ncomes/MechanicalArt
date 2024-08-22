import os

from mca.mya.thirdpartytools.MetaHumanDNACalibrationmain import dna_viewer
from mca.mya.thirdpartytools.MetaHumanDNACalibrationmain.dna_viewer.builder import builder, rig_builder, mesh

from mca.mya.thirdpartytools.MetaHumanDNACalibrationmain.lib.Maya2022.windows import dna, dnacalib
import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMaya as om1
from mca.common.project import paths, project_paths
from mca.mya.modeling import vert_utils
from mca.mya.rigging import skin_utils
from mca.common import log
logger = log.MCA_LOGGER

MH_DIR = r"Python\framework\packages\mca-maya\mca\mya\thirdpartytools\MetaHumanDNACalibrationmain"
ROOT_MH_DIR = os.path.normpath(os.path.join(project_paths.MCA_PROJECT_ROOT, MH_DIR))
MH_DATA_DIR = os.path.join(ROOT_MH_DIR, 'data')


def load_dna_reader(path):
    stream = dna.FileStream(path, dna.FileStream.AccessMode_Read, dna.FileStream.OpenMode_Binary)
    reader = dna.BinaryStreamReader(stream, dna.DataLayer_All)
    reader.read()
    if not dna.Status.isOk():
        status = dna.Status.get()
        raise RuntimeError(f"Error loading DNA: {status.message}")
    return reader


def save_dna(reader, dna_path):
    stream = dna.FileStream(
        dna_path,
        dna.FileStream.AccessMode_Write,
        dna.FileStream.OpenMode_Binary,
    )
    writer = dna.BinaryStreamWriter(stream)
    writer.setFrom(reader)
    writer.write()

    if not dna.Status.isOk():
        status = dna.Status.get()
        raise RuntimeError(f"Error saving DNA: {status.message}")


def get_mesh_vertex_positions_from_scene(meshName):
    if pm.objExists(meshName):
        sel = om1.MSelectionList()
        sel.add(meshName)

        dag_path = om1.MDagPath()
        sel.getDagPath(0, dag_path)

        mf_mesh = om1.MFnMesh(dag_path)
        positions = om1.MPointArray()

        mf_mesh.getPoints(positions, om1.MSpace.kObject)
        return [
            [positions[i].x, positions[i].y, positions[i].z]
            for i in range(positions.length())
        ]
    else:
        print(f'{meshName} not found')
        return []

def run_joints_command(reader, calibrated):
    # Making arrays for joints' transformations and their corresponding mapping arrays
    joint_translations = []
    joint_rotations = []

    for i in range(reader.getJointCount()):
        joint_name = reader.getJointName(i)

        translation = cmds.xform(joint_name, query=True, translation=True)
        joint_translations.append(translation)

        rotation = cmds.joint(joint_name, query=True, orientation=True)
        joint_rotations.append(rotation)

    # This is step 5 sub-step a
    set_new_joints_translations = dnacalib.SetNeutralJointTranslationsCommand(joint_translations)
    # This is step 5 sub-step b
    set_new_joints_rotations = dnacalib.SetNeutralJointRotationsCommand(joint_rotations)

    # Abstraction to collect all commands into a sequence, and run them with only one invocation
    commands = dnacalib.CommandSequence()
    # Add vertex position deltas (NOT ABSOLUTE VALUES) onto existing vertex positions
    commands.add(set_new_joints_translations)
    commands.add(set_new_joints_rotations)

    commands.run(calibrated)
    # Verify that everything went fine
    if not dna.Status.isOk():
        status = dna.Status.get()
        raise RuntimeError(f"Error run_joints_command: {status.message}")


def run_vertices_command(
    calibrated, old_vertices_positions, new_vertices_positions, mesh_index
):
    # Making deltas between old vertices positions and new one
    deltas = []
    for new_vertex, old_vertex in zip(new_vertices_positions, old_vertices_positions):
        delta = []
        for new, old in zip(new_vertex, old_vertex):
            delta.append(new - old)
        deltas.append(delta)

    # This is step 5 sub-step c
    new_neutral_mesh = dnacalib.SetVertexPositionsCommand(
        mesh_index, deltas, dnacalib.VectorOperation_Add
    )
    commands = dnacalib.CommandSequence()
    # Add nex vertex position deltas (NOT ABSOLUTE VALUES) onto existing vertex positions
    commands.add(new_neutral_mesh)
    commands.run(calibrated)

    # Verify that everything went fine
    if not dna.Status.isOk():
        status = dna.Status.get()
        raise RuntimeError(f"Error run_vertices_command: {status.message}")


def assemble_mh_head_rig(dna_path, lod_list):
    char_dna = dna_viewer.DNA(dna_path)
    config = dna_viewer.RigConfig(
        gui_path=os.path.join(MH_DATA_DIR,' gui.ma'),
        analog_gui_path=os.path.join(MH_DATA_DIR, 'analog_gui.ma'),
        aas_path=os.path.join(MH_DATA_DIR, "additional_assemble_script.py"),
    )
    # dna_builder = builder.Builder(dna=char_dna, config=config)
    # dna_builder.build_meshes_by_lod_list(lod_list)
    rig_builder.RigBuilder(char_dna, config)._build_by_lod_list(lod_list)


def update_expression_by_name(input_dna_path, control_name, output_dna_path=None):
    if not output_dna_path:
        output_dna_path = input_dna_path

    dna_reader = load_dna_reader(input_dna_path)
    calibrated = dnacalib.DNACalibDNAReader(dna_reader)
    output_stream = dna.FileStream(output_dna_path, dna.FileStream.AccessMode_Write, dna.FileStream.OpenMode_Binary)
    writer = dna.BinaryStreamWriter(output_stream)
    writer.setFrom(dna_reader)
    joints = []
    joints_group_dict = {}

    joint_count = calibrated.getJointCount()
    for x in range(joint_count):
        joint_name = calibrated.getJointName(x)
        joints.append(joint_name)

    joint_group_count = calibrated.getJointGroupCount()
    for group_index in range(joint_group_count - 1):
        joint_index = calibrated.getJointGroupJointIndices(group_index)
        group_joints = []
        for x in joint_index:
            joint_name = joints[int(x)]
            group_joints.append(joint_name)
        joints_group_dict[group_index] = group_joints

    attr_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    for joint_group, joint_indices_list in joints_group_dict.items():
        joint_output_indices = calibrated.getJointGroupOutputIndices(joint_group)  # joint
        joint_input_indices = calibrated.getJointGroupInputIndices(joint_group)  # raw  ctrl

        # within group get values related to the ctrl expression
        # from output indices /9 get joint
        update_value_list = []

        row_count = len(joint_output_indices)
        col_count = len(joint_input_indices)
        value_table = calibrated.getJointGroupValues(joint_group)
        len(value_table)

        for row in range(row_count):
            output_index = joint_output_indices[row]
            joint_index = output_index // 9
            joint_name = calibrated.getJointName(joint_index)
            attr_index = output_index % 9
            attr = attr_list[attr_index]

            # n_attr_list = calibrated.getNeutralJointTranslation(joint_index) +  calibrated.getNeutralJointRotation(joint_index) + [1, 1, 1]
            n_attr_list = calibrated.getNeutralJointTranslation(joint_index) + [0, 0, 0, 1, 1, 1]
            n_attr = n_attr_list[attr_index]
            # from input indices get ctrl expression
            for col in range(col_count):
                input_index = joint_input_indices[col]
                if calibrated.getRawControlName(input_index) == control_name:
                    current_attr_val = cmds.getAttr(f'{joint_name}.{attr}')
                    delta = current_attr_val - n_attr
                    value_table[row * col_count + col] = delta

        writer.setJointGroupValues(joint_group, value_table)
    # TODO: This shouldn't automatically write (probably)
    writer.write()


def get_full_blendshape_list_from_calibrated(calibrated_dna):
    blendshape_channel_count = calibrated_dna.getBlendShapeChannelCount()
    blendshape_list = []
    for blendshape_channel_index in range(blendshape_channel_count):
        channel_name = calibrated_dna.getBlendShapeChannelName(blendshape_channel_index)
        blendshape_list.append(channel_name)
    return blendshape_list



def get_blendshape_list_for_mesh(mesh_index, char_dna, calibrated_dna, prefix):
    blendshape_list = get_full_blendshape_list_from_calibrated(calibrated_dna)
    maya_mesh = mesh.MayaMesh(mesh_index=mesh_index,
                              dna=char_dna,
                              blend_shape_group_prefix=prefix,
                              blend_shape_name_postfix=prefix,
                              skin_cluster_suffix=prefix)
    mesh_blendshapes = maya_mesh.dna.get_blend_shapes(maya_mesh.mesh_index)
    return_blendshapes = []
    for blend_shape in mesh_blendshapes:
        blendshape_name = blendshape_list[blend_shape.channel]
        return_blendshapes.append(blendshape_name)
    return return_blendshapes

def get_all_meshes_from_calibrated(calibrated_dna):
    all_meshes = []
    mesh_count = calibrated_dna.getMeshCount()
    for mesh_index in range(mesh_count):
        mesh_name = calibrated_dna.getMeshName(mesh_index)
        all_meshes.append(mesh_name)
    return all_meshes

def set_new_mh_face_joint_positions(old_head_mesh,
                                    new_head_mesh,
                                    reader,
                                    calibrated_data):
    facial_root_joint = 'FACIAL_C_FacialRoot'
    jnt_vert_dict = {}
    for jnt in reversed(pm.listRelatives(facial_root_joint, ad=True, type=pm.nt.Joint)):
        if any(pm.listRelatives(jnt, ad=True, type=pm.nt.Joint)):
            continue
        closest_vert = vert_utils.get_closest_vertex_to_object(pm.PyNode(old_head_mesh), jnt)
        jnt_vert_dict[jnt.name()] = closest_vert
    remove_connection_list = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX',
                              'scaleY', 'scaleZ']
    for jnt_name, vert_num in jnt_vert_dict.items():
        connections = pm.listConnections(jnt_name, source=True, destination=False, plugs=True)
        for connection in connections:
            connection_dest = pm.listConnections(connection, source=False, destination=True, plugs=True)
            if connection_dest:
                connection_dest = connection_dest[0]
                if connection_dest.name().split('.')[-1] in remove_connection_list:
                    connection // connection_dest

        pos = pm.xform(f'{new_head_mesh.name()}.vtx[{vert_num}]', q=True, t=True, ws=True)
        jnt = pm.PyNode(jnt_name)
        jnt_par = jnt.getParent()
        jnt.setParent(w=True)
        jnt.tx.set(pos[0])
        jnt.ty.set(pos[1])
        jnt.tz.set(pos[2])
        jnt.setParent(jnt_par)
    run_joints_command(reader, calibrated_data)


def update_mh_face_blendshape(char_dna,
                      calibrated_data,
                      new_blendshape,
                      main_mesh,
                      blendshape_name,
                              dna_path,
                              reader):

    # Interpolate blend shape target deltas between original DNA and below specified deltas
    # ¯\_(?)_/¯
    # Deltas in [[x, y, z], [x, y, z], [x, y, z]] format

    # Weights for interpolation between original deltas and above defined deltas
    # 1.0 == take the new value completely, 0.0 means keep the old value
    # Format: [Delta-0-Mask, Delta-1-Mask, Delta-2-Mask]
    if isinstance(main_mesh, str):
        mesh_name = main_mesh
    else:
        mesh_name = main_mesh.name()
    blendnode = pm.blendShape(new_blendshape, main_mesh, n=f'TEMP_DELETE_ME_blendshape')[0]
    pm.setAttr(f'{blendnode}.{new_blendshape.name()}', 1)

    vertex_deltas = cmds.getAttr(f'{blendnode.name()}.inputTarget[0].inputTargetGroup[0].inputPointsTarget')
    vertex_indices = cmds.getAttr(f'{blendnode.name()}.inputTarget[0].inputTargetGroup[0].inputComponentsTarget')
    flattened_indices = []

    for item in vertex_indices:
        vertices = item.split('vtx[')[1].split(']')[0]
        if ':' in vertices:
            vertex_range = []
            start_vertex, end_vertex = vertices.split(':')
            for vertex_number in range(int(start_vertex), int(end_vertex) + 1):
                vertex_range.append(vertex_number)
        else:
            vertex_range = [int(vertices)]
        flattened_indices += vertex_range
    deltas_formatted = []
    for x in vertex_deltas:
        delta_list = [x[0], x[1], x[2]]
        deltas_formatted.append(delta_list)
    pm.delete(blendnode)

    all_bshapes = []

    blendshape_channel_count = calibrated_data.getBlendShapeChannelCount()
    found_index = None
    for blendshape_channel_index in range(blendshape_channel_count):
        channel_name = calibrated_data.getBlendShapeChannelName(blendshape_channel_index)
        all_bshapes.append(channel_name)
        if channel_name == blendshape_name:
            found_index = blendshape_channel_index
            break
    mesh_list = get_all_meshes_from_calibrated(calibrated_data)
    mesh_index = mesh_list.index(mesh_name)
    maya_mesh = mesh.MayaMesh(mesh_index=mesh_index, dna=char_dna, blend_shape_group_prefix=mesh_name,
                              blend_shape_name_postfix=mesh_name, skin_cluster_suffix=mesh_name)
    blend_shapes = maya_mesh.dna.get_blend_shapes(maya_mesh.mesh_index)
    found_target_index = None
    for x, blend_shape in enumerate(blend_shapes):
        if blend_shape.channel == found_index:
            found_target_index = x
    if not found_target_index:
        logger.warning('Could not find target index')
        return
    masks = [1.0 for x in deltas_formatted]
    setBlendShapesM0B0 = dnacalib.SetBlendShapeTargetDeltasCommand(mesh_index,  # mesh index
                                                                   found_target_index,  # blend shape target index
                                                                   deltas_formatted,
                                                                   flattened_indices,
                                                                   masks,
                                                                   dnacalib.VectorOperation_Interpolate)
    commands = dnacalib.CommandSequence()
    # Add nex vertex position deltas (NOT ABSOLUTE VALUES) onto existing vertex positions
    commands.add(setBlendShapesM0B0)
    commands.run(calibrated_data)
    save_dna(calibrated_data, dna_path)

def clear_mh_face_blendshape_by_name(char_dna,
                      calibrated_data,
                      main_mesh,
                      blendshape_name,
                              dna_path):
    if isinstance(main_mesh, str):
        mesh_name = main_mesh
    else:
        mesh_name = main_mesh.name()
    # vertex_range = pm.polyEvaluate(mesh_name, v=True)
    # flattened_indices = [f'{mesh_name}.vtx[{x}]' for x in range(vertex_range)]
    # deltas_formatted = []
    # for x in flattened_indices:
    #     delta_list = [0.0, 0.0, 0.0]
    #     deltas_formatted.append(delta_list)
    all_bshapes = []
    blendshape_channel_count = calibrated_data.getBlendShapeChannelCount()
    found_index = None
    for blendshape_channel_index in range(blendshape_channel_count):
        channel_name = calibrated_data.getBlendShapeChannelName(blendshape_channel_index)
        all_bshapes.append(channel_name)
        if channel_name == blendshape_name:
            found_index = blendshape_channel_index
            break
    mesh_list = get_all_meshes_from_calibrated(calibrated_data)
    mesh_index = mesh_list.index(mesh_name)
    maya_mesh = mesh.MayaMesh(mesh_index=mesh_index, dna=char_dna, blend_shape_group_prefix=mesh_name,
                              blend_shape_name_postfix=mesh_name, skin_cluster_suffix=mesh_name)
    blend_shapes = maya_mesh.dna.get_blend_shapes(maya_mesh.mesh_index)
    found_target_index = None
    for x, blend_shape in enumerate(blend_shapes):
        if blend_shape.channel == found_index:
            found_target_index = x
    if not found_target_index:
        logger.warning('Could not find target index')
        return
    commands = dnacalib.CommandSequence()
    remove_blendshape_command = dnacalib.RemoveBlendShapeCommand(found_target_index)
    # Add nex vertex position deltas (NOT ABSOLUTE VALUES) onto existing vertex positions
    commands.add(remove_blendshape_command)
    commands.run(calibrated_data)
    save_dna(calibrated_data, dna_path)


def get_mh_face_skinned_joints(joint_list, calibrated_data):
    mesh_name_list = get_all_meshes_from_calibrated(calibrated_data)
    skinned_joint_list = []
    for mesh_name in mesh_name_list:
        if pm.objExists(mesh_name):
            mesh_obj = pm.PyNode(mesh_name)
            skin_cluster = skin_utils.get_skin_cluster_from_geometry(mesh_obj)
            if skin_cluster:
                sc_joints = pm.skinCluster(skin_cluster, q=True, inf=True)
                sc_joint_names = [x.name() for x in sc_joints]
                for sc_joint_name in sc_joint_names:
                    if sc_joint_name in joint_list and sc_joint_name not in skinned_joint_list:
                        skinned_joint_list.append(sc_joint_name)
    return skinned_joint_list

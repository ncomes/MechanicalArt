#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains utilities for working with Maya materials and shader groups.
"""

# System global imports
import os
# software specific imports
import pymel.core as pm
import maya.api.OpenMaya as om2
#  python imports
from mca.common import log
from mca.common.paths import path_utils
from mca.common.utils import lists
from mca.mya.utils.om import om_utils
from mca.mya.utils import naming, node_util

logger = log.MCA_LOGGER


def get_object_material_face_dict(node):
    """
    From a given node return the material application dictionary

    :param Transform node: A shaped transform node we wish to query material details about.
    :return: A dictionary of material nodes to a list of faces it is applied to.
    :rtype: dict{PyNode:list[int...]}
    """

    if not isinstance(node, pm.nt.Transform) or not node.getShape():
        logger.warning(f'{node}, an object must be a valid shape node.')
        return {}
    m_dag_path, _ = om_utils.pynode_to_om2_mobject_mdag_path(node)
    m_dag_path = om2.MDagPath(m_dag_path)
    fnm = om2.MFnMesh(m_dag_path.extendToShape().node())

    shading_engine_list, face_list = fnm.getConnectedShaders(0)
    material_list = []
    for shading_engine in shading_engine_list:
        m_dep = om2.MFnDependencyNode(shading_engine)
        m_plug = m_dep.findPlug("surfaceShader", True)
        try:
            material_list.append(pm.PyNode(om2.MFnDependencyNode(m_plug.connectedTo(True, True)[0].node()).name()))
        except:
            logger.warning(log_string='ShaderEngine without a surface material')
            material_list.append('')

    shader_face_dict = {}
    for material_node in material_list:
        shader_face_dict[material_node] = []

    for index, material_index in enumerate(face_list):
        shader_face_dict[material_list[material_index]].append(index)
    return shader_face_dict


def assign_material(material_node, node_list):
    """
    Apply material to assignment.

    :param PyNode material_node: Material to assign
    :param list[PyNodes] node_list: A list of trasnforms, or faces to apply the given material to.
    """
    shading_groups = material_node.outColor.listConnections(destination=True, type=pm.nt.ShadingEngine)

    if not shading_groups:
        # The material is not associated with any shading group, so
        # we'll create one now, and & connect this material to it.
        shading_groups = [pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{material_node.name()}SG')]
        material_node.outColor.connect(shading_groups[0].surfaceShader, force=True)

    shading_group = lists.get_first_in_list(shading_groups)
    pm.sets(shading_group, edit=True, forceElement=node_list)


def create_texture(file_path, name=None):
    """
    Creates new file node and assigns texture from file_path.

    :param str file_path: path to texture file
    :param str name: The name to be used for the file/place2dTexture nodes.
    :return: The File pynode that represents the Maya converted texture.
    :rtype: File
    """

    file_node = None
    place_texture_node = None
    split_path = os.path.basename(file_path).split('.')
    if not name:
        name = split_path[0]

    name = naming.make_maya_safe_name(name)

    if name:
        file_node = lists.get_first_in_list(pm.ls(f'{name}_file', r=True, type=pm.nt.File))
        place_texture_node = lists.get_first_in_list(pm.ls(f'{name}_place2dTexture', r=True, type=pm.nt.Place2dTexture))

    if not file_node:
        if name:
            file_node = pm.shadingNode(pm.nt.File, asTexture=True, name=f'{name}_file')
        else:
            file_node = pm.shadingNode(pm.nt.File, asTexture=True)

    if not place_texture_node:
        if name:
            place_texture_node = pm.shadingNode(pm.nt.Place2dTexture, asUtility=True, name=f'{name}_place2dTexture')
        else:
            place_texture_node = pm.shadingNode(pm.nt.Place2dTexture, asUtility=True)

        place_texture_node.coverage >> file_node.coverage
        place_texture_node.translateFrame >> file_node.translateFrame
        place_texture_node.rotateFrame >> file_node.rotateFrame
        place_texture_node.mirrorU >> file_node.mirrorU
        place_texture_node.mirrorV >> file_node.mirrorV
        place_texture_node.stagger >> file_node.stagger
        place_texture_node.wrapU >> file_node.wrapU
        place_texture_node.wrapV >> file_node.wrapV
        place_texture_node.repeatUV >> file_node.repeatUV
        place_texture_node.offset >> file_node.offset
        place_texture_node.rotateUV >> file_node.rotateUV
        place_texture_node.noiseUV >> file_node.noiseUV
        place_texture_node.vertexUvOne >> file_node.vertexUvOne
        place_texture_node.vertexUvTwo >> file_node.vertexUvTwo
        place_texture_node.vertexUvThree >> file_node.vertexUvThree
        place_texture_node.vertexCameraOne >> file_node.vertexCameraOne

        place_texture_node.outUV >> file_node.uv
        place_texture_node.outUvFilterSize >> file_node.uvFilterSize
    file_node.fileTextureName.set(file_path)
    if len(split_path) > 2:
        try:
            mari_val = int(split_path[-2])
            if mari_val:
                if mari_val > 1001 or os.path.exists(file_path.replace(str(mari_val), str(mari_val+1))):
                    file_node.setAttr('uvTilingMode', 3)
                    file_node.setAttr('uvTileProxyQuality', 1)
                    # Preview generation fails when switched to MARI uv tiling.
                    pm.evalDeferred(pm.mel.generateUvTilePreview(file_node.name()))
        except:
            pass

    if not file_node.fileHasAlpha.get():
        file_node.setAttr('alphaIsLuminance', True)
    return file_node


def create_normal(normal_path, name=None):
    """
    Create a new bump2d node from the normal path, and return that for use.

    :param str normal_path: The path to a given normal path.
    :param str name: The name to be used for the file/place2dTexture nodes.
    :return: The bump2d pynode that represents the Maya converted texture.
    :rtype: Bump2d
    """

    if not name:
        name = os.path.basename(normal_path).split('.')[0]

    name = naming.make_maya_safe_name(name)

    file_node = create_texture(normal_path, name=name)

    bump2d_node = node_util.create_or_find(f'{name}_bump2d', pm.nt.Bump2d)

    bump2d_node.setAttr('bumpInterp', 1)

    bump2d_node.disconnectAttr('bumpValue')
    file_node.outAlpha >> bump2d_node.bumpValue
    return bump2d_node


def create_basic_blinn(diffuse_path=None, default_color=None, name=None):
    """
    Create a new mya blinn material node for use in the scene.

    :param str diffuse_path: A path to a given diffuse file.
    :param list[float, float, float] default_color: Float3 that represents the RGB values of the shader, this will be applied if a diffuse map is not passed.
    :param str name: The name of the new material node. If not it will try to generate from the diffuse path, or a generic name.
    :return: The newly created material node
    """

    default_color = default_color or [.5, .5, .5]

    base_name = name or naming.make_maya_safe_name(os.path.basename(diffuse_path).rpartition('_')[0] or 'basicBlinn')
    material_node = lists.get_first_in_list(pm.ls(base_name, r=True, type=pm.nt.Blinn)) if base_name != 'basicBlinn' else None
    if not material_node:
        material_node = pm.shadingNode(pm.nt.Blinn, asShader=True, name=base_name)

    if not material_node.eccentricity.connections(s=True):
        material_node.eccentricity.set(0.8)
    if not material_node.specularRollOff.connections(s=True):
        material_node.specularRollOff.set(0.5)
    if not material_node.specularRollOff.connections(s=True):
        material_node.diffuse.set(1.0)

    if not material_node.color.connections(s=True) and not material_node.colorR.connections(s=True):
        material_node.color.set(default_color)

    if diffuse_path:
        file_node = create_texture(diffuse_path)
        material_node.disconnectAttr('color')
        file_node.outColor >> material_node.color

        if not material_node.hasAttr('texture_path'):
            material_node.addAttr('texture_path', dt='string')
        material_node.setAttr('texture_path', path_utils.to_relative_path(diffuse_path))
    return material_node


def consolidate_materials(material_node_list, rebuild=True, simple_material=False):
    """
    For a list of materials convert them to  defaults and apply them in place of the original stuff.

    :param list[PyNode] material_node_list: A list of material nodes to reprocess.
        NOTE: These needed to be marked up with a texture path.
    :param bool rebuild: If materials should be rebuilt even if they already exist.
    :param bool simple_material: If materials should be built with only diffuse and alpha.
        NOTE: For increased performance/stability it's recommended to use this option.
    """

    things_to_delete = []
    for material_node in material_node_list:
        if not material_node.hasAttr('texture_path'):
            continue

        if isinstance(material_node, pm.nt.Blinn) and material_node.hasAttr('texture_path'):
            DefaultMaterial(path_utils.to_full_path(material_node.getAttr('texture_path')), simple_material=simple_material, rebuild=rebuild)
            continue

        material_node.rename('temp')
        file_path = path_utils.to_full_path(material_node.getAttr('texture_path'))
        if not os.path.exists(file_path):
            continue

        mca_material = DefaultMaterial(file_path, simple_material=simple_material, rebuild=rebuild)
        replace_material(material_node, mca_material.material_node)


def replace_material(source_material, replacement_material):
    """
    Replace the usage of one material with another.
    NOTE: This will remove the original material and its shader groups.

    :param PyNode source_material: The material we want to replace.
    :param PyNode replacement_material: The material we will be replacing with.
    """
    things_to_delete = [source_material]

    target_shading_group = lists.get_first_in_list(replacement_material.listConnections(type=pm.nt.ShadingEngine))
    if not target_shading_group:
        target_shading_group = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{replacement_material.name()}SG')
        replacement_material.outColor.connect(target_shading_group.surfaceShader, force=True)

    for og_sg in source_material.listConnections(type=pm.nt.ShadingEngine):
        if not og_sg:
            return

        og_sg.rename('tempSG')
        for x in og_sg.members():
            og_sg.removeMember(x)
            target_shading_group.addMember(x)

        things_to_delete.append(og_sg)
    pm.delete(things_to_delete)


def refresh_file_nodes():
    """
    Resets texture paths to local paths.

    """
    for file_node in pm.ls(type=pm.nt.File):
        file_node.fileTextureName.set(path_utils.to_relative_path(file_node.getAttr('fileTextureName')))
        pm.mel.generateUvTilePreview(file_node.name())


class DefaultMaterial(object):
    diffuse_path = None
    rida_path = None
    normal_path = None
    mra_path = None
    orme_path = None
    material_node = None
    base_name = None

    def __init__(self, file_path, simple_material=False, rebuild=False):
        """
        This is a generic shader builder that works with Diffuse, MRA, and Normal maps.

        :param str file_path: The path to one of the three supported maps.
        :param bool simple_material: If materials should be built with only diffuse and alpha.
        :param bool rebuild: If materials should be rebuilt even if they already exist.
        """

        self.initialize_textures(file_path)
        self.material_node = self.build(simple_material=simple_material, rebuild=rebuild)

        hardware_globals_node = lists.get_first_in_list(pm.ls(type=pm.nt.HardwareRenderingGlobals))
        hardware_globals_node.transparencyAlgorithm.set(3)

    def initialize_textures(self, file_path=None):
        """
        This runs during initialization and collects our used maps. If not found the material will default to a light grey.

        :param str file_path: The path to one of the three supported maps.
        """

        base_dir = os.path.dirname(file_path)
        split_path = file_path.split('.')
        identifier = None
        if len(split_path) > 2:
            identifier = split_path[-2]
        self.base_name = os.path.basename(file_path).rpartition('_')[0]
        for file_name in os.listdir(base_dir):
            if identifier and identifier not in file_name:
                continue

            if file_name.startswith(f'{self.base_name}_D'):
                self.diffuse_path = os.path.join(base_dir, file_name)
            if file_name.startswith(f'{self.base_name}_RIDA'):
                self.rida_path = os.path.join(base_dir, file_name)
            if file_name.startswith(f'{self.base_name}_N'):
                self.normal_path = os.path.join(base_dir, file_name)
            if file_name.startswith(f'{self.base_name}_MRA'):
                self.mra_path = os.path.join(base_dir, file_name)
            if file_name.startswith(f'{self.base_name}_ORME'):
                self.orme_path = os.path.join(base_dir, file_name)

                # strip off the T_ leading characters if they are in the path name.
        self.base_name = naming.make_maya_safe_name(self.base_name[2:]) if self.base_name.startswith('T_') else naming.make_maya_safe_name(self.base_name)

    def build(self, simple_material=False, rebuild=True):
        """
        This connects our found maps to the blinn shader node.

        :param bool simple_material: If materials should be built with only diffuse and alpha.
        :param bool rebuild: If materials should be rebuilt even if they already exist.
        :return:
        """

        if rebuild or not self.material_node or not self.material_node.exists():
            if self.diffuse_path:
                diffuse_file = create_texture(self.diffuse_path)
                self.material_node = create_basic_blinn(self.diffuse_path, name=f'{self.base_name}')
                rebuild = True
                use_alpha = diffuse_file.getAttr('fileHasAlpha')
                if use_alpha:
                    reverse_node = lists.get_first_in_list(pm.ls(f'{self.base_name}_reverse', r=True, type=pm.nt.Reverse))
                    if not reverse_node:
                        reverse_node = pm.createNode(pm.nt.Reverse, n=f'{self.base_name}_reverse')
                    reverse_node.disconnectAttr('inputX')
                    diffuse_file.outAlpha >> reverse_node.inputX
                    for key in 'RGB':
                        self.material_node.disconnectAttr(f'transparency{key}')
                        reverse_node.outputX >> self.material_node.attr(f'transparency{key}')
            elif self.rida_path:
                self.material_node = create_basic_blinn(None, name=f'{self.base_name}')
                if not self.material_node.hasAttr('texture_path'):
                    self.material_node.addAttr('texture_path', dt='string')
                self.material_node.setAttr('texture_path', path_utils.to_relative_path(self.rida_path))

                file_node = create_texture(self.rida_path)
                color_remap = node_util.create_or_find(f'{self.base_name}_color_remap', pm.nt.RemapValue)
                color_remap.setAttr('outputMax', .1)
                color_remap.setAttr('outputMax', .25)
                color_remap.disconnectAttr('inputValue')
                file_node.outColorG >> color_remap.inputValue
                for key in 'RGB':
                    self.material_node.disconnectAttr(f'color{key}')
                    color_remap.outValue >> self.material_node.attr(f'color{key}')

                rebuild = True
                use_alpha = file_node.getAttr('fileHasAlpha')
                if use_alpha:
                    rida_reverse = node_util.create_or_find(f'{self.base_name}_reverse', pm.nt.Reverse)
                    rida_file = create_texture(self.rida_path)
                    for key in 'XYZ':
                        rida_reverse.disconnectAttr(f'input{key}')
                        rida_file.outAlpha >> rida_reverse.attr(f'input{key}')

                    self.material_node.disconnectAttr('transparency')
                    rida_reverse.output >> self.material_node.transparency

                    # technically this handles some spec stuff but it looks really broken without.
                    spec_remap = node_util.create_or_find(f'{self.base_name}_spec_remap', pm.nt.RemapValue)
                    spec_remap.setAttr('outputMax', .25)
                    spec_remap.disconnectAttr('inputValue')
                    rida_file.outAlpha >> spec_remap.inputValue

                    self.material_node.disconnectAttr('eccentricity')
                    spec_remap.outValue >> self.material_node.eccentricity

        if not rebuild:
            return self.material_node

        if not simple_material:
            if self.normal_path:
                # Normal
                normal_bump2d_node = create_normal(self.normal_path)
                self.material_node.disconnectAttr('normalCamera')
                normal_bump2d_node.outNormal >> self.material_node.normalCamera
            else:
                # break normal connections.
                self.material_node.disconnectAttr('normalCamera')

            if self.mra_path or self.orme_path:
                if self.mra_path:
                    mra_file_node = create_texture(self.mra_path)
                elif self.orme_path:
                    mra_file_node = create_texture(self.orme_path)

                # Metalness
                remap_node = lists.get_first_in_list(pm.ls(f'{self.base_name}_remap', r=True, type=pm.nt.RemapValue))
                if not remap_node:
                    remap_node = pm.createNode(pm.nt.RemapValue, n=f'{self.base_name}_remap')
                remap_node.disconnectAttr('inputValue')
                if self.mra_path:
                    mra_file_node.outColorR >> remap_node.inputValue
                elif self.orme_path:
                    mra_file_node.outColorB >> remap_node.inputValue
                # clamp down the metalness value reduce surface shine.
                remap_node.setAttr('outputMax', .25)

                reverse_node = lists.get_first_in_list(pm.ls(f'{self.base_name}_reverse', r=True, type=pm.nt.Reverse))
                if not reverse_node:
                    reverse_node = pm.createNode(pm.nt.Reverse, n=f'{self.base_name}_reverse')

                diffuse_file = create_texture(self.diffuse_path)
                reverse_node.disconnectAttr('inputX')
                if use_alpha:
                    diffuse_file.outAlpha >> reverse_node.inputX
                else:
                    reverse_node.inputX.set(0)

                multi_node = lists.get_first_in_list(
                    pm.ls(f'{self.base_name}_multi', r=True, type=pm.nt.MultiplyDivide))
                if not multi_node:
                    multi_node = pm.createNode(pm.nt.MultiplyDivide, n=f'{self.base_name}_multi')

                multi_node.disconnectAttr('input1X')
                reverse_node.outputX >> multi_node.input1X
                multi_node.disconnectAttr('input1Y')
                reverse_node.outputX >> multi_node.input1Y
                multi_node.disconnectAttr('input2X')
                remap_node.outValue >> multi_node.input2X

                self.material_node.disconnectAttr('eccentricity')
                multi_node.outputX >> self.material_node.eccentricity

                # Roughness
                remap_node = lists.get_first_in_list(pm.ls(f'{self.base_name}_R_remap', r=True, type=pm.nt.RemapValue))
                if not remap_node:
                    remap_node = pm.createNode(pm.nt.RemapValue, n=f'{self.base_name}_R_remap')
                remap_node.disconnectAttr('inputValue')
                mra_file_node.outColorG >> remap_node.inputValue
                # clamp down the roughness to reduce spot shine.
                remap_node.setAttr('outputMax', .25)

                multi_node.disconnectAttr('input2Y')
                remap_node.outValue >> multi_node.input2Y
                self.material_node.disconnectAttr('specularRollOff')
                multi_node.outputY >> self.material_node.specularRollOff

                # Ambient Occlusion
                for key in 'RGB':
                    self.material_node.disconnectAttr(f'ambientColor{key}')
                    if self.mra_path:
                        material_attr = mra_file_node.outColorB
                    elif self.orme_path:
                        material_attr = mra_file_node.outColorR
                    material_attr >> self.material_node.attr(f'ambientColor{key}')

            elif self.rida_path:
                # RIDA spec
                rida_file = create_texture(self.rida_path)
                rida_remap = node_util.create_or_find(f'{self.base_name}_remap_ecc', pm.nt.RemapValue)
                rida_remap.setAttr('outputMax', .5)
                rida_remap.disconnectAttr('inputValue')
                rida_file.outColorB >> rida_remap.inputValue

                self.material_node.disconnectAttr('specularRollOff')
                rida_remap.outValue >> self.material_node.specularRollOff
            else:
                # break spec connections.
                self.material_node.disconnectAttr('eccentricity')
                self.material_node.disconnectAttr('specularRollOff')
        return self.material_node


import unreal


def set_mi_texture(mi_asset, param_name, tex_path):
    if not unreal.EditorAssetLibrary.does_asset_exist(tex_path):
        unreal.log_warning("Can't find texture: " + tex_path)
        return False
    tex_asset = unreal.EditorAssetLibrary.find_asset_data(tex_path).get_asset()
    return unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, param_name, tex_asset)


unreal.log("---------------------------------------------------")
AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
MaterialEditingLibrary = unreal.MaterialEditingLibrary
EditorAssetLibrary = unreal.EditorAssetLibrary
base_mtl = unreal.EditorAssetLibrary.find_asset_data("/Game/Environment/Cave/Materials/M_CaveBase")

# Iterate over selected meshes
sel_assets = unreal.EditorUtilityLibrary.get_selected_assets()
for sm_asset in sel_assets:
    if sm_asset.get_class().get_name() != "StaticMesh":
        continue  # skip non-static-meshes

    asset_name = sm_asset.get_name()
    if asset_name.startswith("S_"):
        asset_name = asset_name[2:]  # Store mesh name without prefix
    asset_folder = unreal.Paths.get_path(sm_asset.get_path_name())
    base_folder = asset_folder[:-7]  # get base folder (subtract "Meshes" from base path)
    mtl_folder = base_folder + "/Materials/"
    tex_folder = base_folder + "/Textures/"

    # create folder for materials if not exist
    if not unreal.EditorAssetLibrary.does_directory_exist(mtl_folder):
        unreal.EditorAssetLibrary.make_directory(mtl_folder)
    # name of material instance for this mesh
    mi_name = "MI_" + asset_name
    mi_full_path = mtl_folder + mi_name
    # Check if material instance already exists
    if EditorAssetLibrary.does_asset_exist(mi_full_path):
        mi_asset = EditorAssetLibrary.find_asset_data(mi_full_path).get_asset()
        unreal.log("Asset already exists")
    else:
        mi_asset = AssetTools.create_asset(mi_name, mtl_folder, unreal.MaterialInstanceConstant,
                                           unreal.MaterialInstanceConstantFactoryNew())
        # set material instance parameters!
    MaterialEditingLibrary.set_material_instance_parent(mi_asset, base_mtl.get_asset())  # set parent material
    MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi_asset, "Desaturation",
                                                                        0.3)  # set scalar parameter
    # find textures for this mesh
    set_mi_texture(mi_asset, "Base Color", tex_folder + "T_" + asset_name + "_basecolor")
    set_mi_texture(mi_asset, "Masks Map", tex_folder + "T_" + asset_name + "_masks")
    set_mi_texture(mi_asset, "Normal", tex_folder + "T_" + asset_name + "_normal")
    set_mi_texture(mi_asset, "BentNormal", tex_folder + "T_" + asset_name + "_Bentnormal")
    # set new material instance on static mesh
    sm_asset.set_material(0, mi_asset)





def buildSelectedAssets(folderPath,fileNames):
    """
    Sets up static mesh, material instances, and textures.  Args passed in by import script.
    """
    # lists to hold new assets
    textures = []
    geo = []
    materialInstances = []
    # create asset tools instance
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    EAL = unreal.EditorAssetLibrary()
    # hard coded path to parent material
    materialParent = EAL.load_asset('/Game/Meshes/ImportTest/M_parent')
    # get all assets in folder path
    for assetPath in EAL.list_assets(folderPath):
        # clean up asset path
        assetPath = assetPath.split('.')[0]
        # identify newly import assets
        # load assets, located file import path, and compare to file import paths passed in from import script.
        asset = EAL.load_asset(assetPath)
        try:
            assetImportData = asset.get_editor_property('asset_import_data')
            importfilePath = assetImportData.get_first_filename()
            if importfilePath in fileNames:
                if isinstance(asset, unreal.StaticMesh):
                    geo.append(asset)
                if isinstance(asset, unreal.Texture):
                    textures.append(asset)
        except AttributeError: # not all assets have asset import data
            pass
    for staticMesh in geo:
        # get asset name from static mesh to find textures later
        assetName = staticMesh.get_name().split('_')[1]
        # iterate over all static materials associated with mesh
        for staticMaterial in staticMesh.static_materials:
            # get the index of the current static material for later
            index = staticMesh.static_materials.index(staticMaterial)
            # locate and delete the default material created on import
            matPath = staticMaterial.material_interface.get_path_name()
            unreal.EditorAssetLibrary.delete_asset(matPath)
            # create new material instance
            materialInstance = assetTools.create_asset(
                staticMaterial.material_slot_name,
                folderPath,
                unreal.MaterialInstanceConstant,
                unreal.MaterialInstanceConstantFactoryNew(),
            )
            materialInstances.append(materialInstance)
            # set parent material
            materialInstance.set_editor_property('parent', materialParent)
            # assign new material instance to correct material slot
            staticMesh.set_material(index, materialInstance)
            # iterate over textures
            for texture in textures:
                # identify textures associated with asset by naming convention
                if assetName in texture.get_name():
                    # get parameter name from texture name - i.e. T_Airconditioner_BC -> BC
                    parameterName = texture.get_name().split('_')[-1]
                    # set up material instance parameter
                    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                        materialInstance,
                        parameterName,
                        texture
                )
    # save all new assets
    newAssets = [geo,textures,materialInstances]
    for list in newAssets:
        for asset in list:
            unreal.EditorAssetLibrary.save_asset(asset.get_path_name())


# Result: Effect Timeline Preview
# Result: Warm Up And Cooldown Use Relative Timeline
# Result: AS NSI_PS_Active
# Result: AS DebugTimeline
# Result: AS_Active
# Result: NSI
# Result: Emissive Eye Adaptation
# Result: Fake Shader Lighting
# Result: Fresnel Lighting
# Result: Use Layer Visualizer
# Result: Disintegration
# Result: Use Emissive
# Result: Use Subsurface Profile
# Result: VisualizeAlbedoCombined
# Result: VisualizeAlbedoBase
# Result: VisualizeAmbientOcclusion
# Result: VisualizeSubsurfaceColor
# Result: VisualizeNormalMapDetail
# Result: VisualizeSubsurfaceDepth
# Result: VisualizeNormalMap
# Result: VisualizeDetailNormalMapFade
# Result: VisualizeSubsurfaceFadeDistance
# Result: Use Detail Color Tint
# Result: Skin Detail Color Invert
# Result: Use Subsurface Distance Fading
# Result: Use Texture UDIMs
# Result: Use Region Collapse
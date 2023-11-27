import unreal
import fnmatch
import os
import re

ea_system = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ls_system = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
eu_system = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
ue_system = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
eas_system = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
le_system = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)


def get_material_slot_names(static_mesh):
    sm_component = unreal.StaticMeshComponent()
    sm_component.set_static_mesh(static_mesh)
    return unreal.StaticMeshComponent.get_material_slot_names(sm_component)


def get_assets_on_actor(actor, only_type=None):
    """
    Gets only actors that are created by directly instancing assets.
    """
    assets = []

    # only get the asset type specified in only_type if it is provided
    if not only_type or only_type == 'StaticMesh':
        for component in actor.get_components_by_class(unreal.StaticMeshComponent):
            if component.static_mesh and actor.get_class().get_name() == 'StaticMeshActor':
                # make sure we only get one unique instance of the asset
                if component.static_mesh not in assets:
                    assets.append(component.static_mesh)

    for component in actor.get_components_by_class(unreal.SkeletalMeshComponent):
        if component.skeletal_mesh:
            # only get the asset type specified in only_type if it is provided
            if not only_type or only_type == 'SkeletalMesh':
                # make sure we only get one unique instance of the asset
                if component.skeletal_mesh not in assets:
                    assets.append(component.skeletal_mesh)

            # only get the asset type specified in only_type if it is provided
            if not only_type or only_type == 'AnimSequence':
                if component.animation_mode == unreal.AnimationMode.ANIMATION_SINGLE_NODE:
                    if component.animation_data and component.animation_data.anim_to_play not in assets:
                        assets.append(component.animation_data.anim_to_play)

    return assets



def select_actors(actors_to_select=[]):
    # unreal.EditorLevelLibrary.set_selected_level_actors(actors_to_select)
    ea_system.set_selected_level_actors(actors_to_select)


def get_selected_actors():
    # return unreal.EditorLevelLibrary.get_selected_level_actors()
    return ea_system.get_selected_level_actors()


def get_asset_actors_in_level():
    """
    Gets actors from the active level that have assets assigned to them.
    """
    actors = []
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    for actor in actor_subsystem.get_all_level_actors():
        if get_assets_on_actor(actor):
            actors.append(actor)
    return actors


def get_asset_actor_by_label(label):
    """
    Gets the asset actor by the given label.
    """
    for actor in get_asset_actors_in_level():
        if label == actor.get_actor_label():
            return actor


def has_asset_actor_with_label(label):
    """
    Checks if the level has actors with the given label.
    """
    for actor in get_asset_actors_in_level():
        if label == actor.get_actor_label():
            return True
    return False


def delete_all_asset_actors():
    """
    Deletes all actors from the active level that have assets assigned to them.
    """
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in get_asset_actors_in_level():
        actor_subsystem.destroy_actor(actor)
        break


def delete_asset_actor_with_label(label):
    """
    Deletes the actor with the given label.
    """
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in get_asset_actors_in_level():
        if label == actor.get_actor_label():
            actor_subsystem.destroy_actor(actor)
            break


def get_material_index_by_name(asset_path, material_name):
    """
    Checks to see if an asset has a complex collision.

    :param str asset_path: The path to the unreal asset.
    :param str material_name: The name of the material.
    :return str: The name of the complex collision.
    """
    mesh = unreal.load_asset(asset_path)
    if mesh.__class__.__name__ == 'SkeletalMesh':
        for index, material in enumerate(mesh.materials):
            if material.material_slot_name == material_name:
                return index
    if mesh.__class__.__name__ == 'StaticMesh':
        for index, material in enumerate(mesh.static_materials):
            if material.material_slot_name == material_name:
                return index
            
def cast(object_to_cast=None, object_class=None):
    try:
        return object_class.cast(object_to_cast)
    except:
        return None
    

def getAllActors(use_selection=False, actor_class=None, actor_tag=None, world=None):
    world = world if world is not None else unreal.EditorLevelLibrary.get_editor_world() # Make sure to have a valid world
    if use_selection:
        selected_actors = get_selected_actors()
        class_actors = selected_actors
        if actor_class:
            class_actors = [x for x in selected_actors if cast(x, actor_class)]
        tag_actors = class_actors
        if actor_tag:
            tag_actors = [x for x in selected_actors if x.actor_has_tag(actor_tag)]
        return [x for x in tag_actors]
    elif actor_class:
        actors = unreal.GameplayStatics.get_all_actors_of_class(world, actor_class)
        tag_actors = actors
        if actor_tag:
            tag_actors = [x for x in actors if x.actor_has_tag(actor_tag)]
        return [x for x in tag_actors]
    elif actor_tag:
        tag_actors = unreal.GameplayStatics.get_all_actors_with_tag(world, actor_tag)
        return [x for x in tag_actors]
    else:
        actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)
        return [x for x in actors]


def spawnBlueprintActor(path='', actor_location=None, actor_rotation=None, actor_scale=None, world=None, properties={}):
    actor_class = unreal.EditorAssetLibrary.load_blueprint_class(path)
    actor_transform = unreal.Transform(actor_location, actor_rotation, actor_scale)
    world = world if world is not None else unreal.EditorLevelLibrary.get_editor_world() # Make sure to have a valid world
    # Begin Spawn
    actor = unreal.GameplayStatics.begin_spawning_actor_from_class(world_context_object=world, actor_class=actor_class, spawn_transform=actor_transform, no_collision_fail=True)
    # Edit Properties
    for x in properties:
        actor.set_editor_property(x, properties[x])
    # Complete Spawn
    unreal.GameplayStatics.finish_spawning_actor(actor=actor, spawn_transform=actor_transform)
    return actor


def createGenericAsset(asset_path='', unique_name=True, asset_class=None, asset_factory=None):
    if unique_name:
        asset_path, asset_name = unreal.AssetToolsHelpers.get_asset_tools().create_unique_asset_name(base_package_name=asset_path, suffix='')
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path=asset_path):
        path = asset_path.rsplit('/', 1)[0]
        name = asset_path.rsplit('/', 1)[1]
        return unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=name, package_path=path, asset_class=asset_class, factory=asset_factory)
    return unreal.load_asset(asset_path)


def showAssetsInContentBrowser(paths=[]):
    unreal.EditorAssetLibrary.sync_browser_to_objects(asset_paths=paths)


def openAssets(paths=[]):
    loaded_assets = [getPackageFromPath(x) for x in paths]
    unreal.AssetToolsHelpers.get_asset_tools().open_editor_for_assets(assets=loaded_assets)


def createDirectory(path=''):
    return unreal.EditorAssetLibrary.make_directory(directory_path=path)


def duplicateDirectory(from_dir='', to_dir=''):
    return unreal.EditorAssetLibrary.duplicate_directory(source_directory_path=from_dir, destination_directory_path=to_dir)


def deleteDirectory(path=''):
    return unreal.EditorAssetLibrary.delete_directory(directory_path=path)


def directoryExist(path=''):
    return unreal.EditorAssetLibrary.does_directory_exist(directory_path=path)


def renameDirectory(from_dir='', to_dir=''):
    return unreal.EditorAssetLibrary.rename_directory(source_directory_path=from_dir, destination_directory_path=to_dir)


def duplicateAsset(from_path='', to_path=''):
    return unreal.EditorAssetLibrary.duplicate_asset(source_asset_path=from_path, destination_asset_path=to_path)


def deleteAsset(path=''):
    return unreal.EditorAssetLibrary.delete_asset(asset_path_to_delete=path)


def assetExist(path=''):
    return unreal.EditorAssetLibrary.does_asset_exist(asset_path=path)


def renameAsset(from_path='', to_path=''):
    return unreal.EditorAssetLibrary.rename_asset(source_asset_path=from_path, destination_asset_path=to_path)


def duplicateAssetDialog(from_path='', to_path='', show_dialog=True):
    splitted_path = to_path.rsplit('/', 1)
    asset_path = splitted_path[0]
    asset_name = splitted_path[1]
    if show_dialog:
        return unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset_with_dialog(asset_name=asset_name, package_path=asset_path, original_object=getPackageFromPath(from_path))
    else:
        return unreal.duplicate_asset.get_asset_tools().duplicate_asset(asset_name=asset_name, package_path=asset_path, original_object=getPackageFromPath(from_path))


def renameAssetDialog(from_path='', to_path='', show_dialog=True):
    splitted_path = to_path.rsplit('/', 1)
    asset_path = splitted_path[0]
    asset_name = splitted_path[1]
    rename_data = unreal.AssetRenameData(asset=getPackageFromPath(from_path), new_package_path=asset_path, new_name=asset_name)
    if show_dialog:
        return unreal.AssetToolsHelpers.get_asset_tools().rename_assets_with_dialog(assets_and_names=[rename_data])
    else:
        return unreal.AssetToolsHelpers.get_asset_tools().rename_assets(assets_and_names=[rename_data])


def saveAsset(path='', force_save=True):
    return unreal.EditorAssetLibrary.save_asset(asset_to_save=path, only_if_is_dirty = not force_save)


def saveDirectory(path='', force_save=True, recursive=True):
    return unreal.EditorAssetLibrary.save_directory(directory_path=path, only_if_is_dirty=not force_save, recursive=recursive)


def getPackageFromPath(path):
    return unreal.load_package(name=path)


def getAllDirtyPackages():
    packages = []
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
        packages.append(x)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages():
        packages.append(x)
    return packages


def saveAllDirtyPackages(show_dialog=False):
    if show_dialog:
        return unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(save_map_packages=True, save_content_packages=True)
    else:
        return unreal.EditorLoadingAndSavingUtils.save_dirty_packages(save_map_packages=True, save_content_packages=True)


def savePackages(packages=[], show_dialog=False):
    if show_dialog:
        return unreal.EditorLoadingAndSavingUtils.save_packages_with_dialog(packages_to_save=packages, only_dirty=False) # only_dirty=False :
    else:                                                                                                                # looks like that it's not
        return unreal.EditorLoadingAndSavingUtils.save_packages(packages_to_save=packages, only_dirty=False)             # working properly at the moment


def buildImportTask(filename='', destination_path='', options=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.set_editor_property('options', options)
    return task


def executeImportTasks(tasks=[]):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    imported_asset_paths = []
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            imported_asset_paths.append(path)
    return imported_asset_paths


def buildStaticMeshImportOptions():
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_as_skeletal', False)  # Static Mesh
    options.set_editor_property('import_animations', False)

    # unreal.FbxMeshImportData
    options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxStaticMeshImportData
    options.static_mesh_import_data.set_editor_property('convert_scene', False)
    options.static_mesh_import_data.set_editor_property('combine_meshes', True)
    options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
    options.static_mesh_import_data.set_editor_property("vertex_color_import_option", unreal.VertexColorImportOption.REPLACE)
    options.static_mesh_import_data.set_editor_property('normal_import_method', unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)
    options.static_mesh_import_data.set_editor_property("build_nanite", False)  # todo add nanite option

    return options


def buildSkeletalMeshImportOptions():
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_as_skeletal', True)  # Skeletal Mesh
    options.set_editor_property('create_physics_asset', False)
    options.set_editor_property('mesh_type_to_import',unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    # options.skeletal_mesh_import_data.set_editor_property("create_materials", False)
    # options.skeletal_mesh_import_data.set_editor_property("find_materials", True)
    options.skeletal_mesh_import_data.set_editor_property('import_content_type',unreal.FBXImportContentType.FBXICT_ALL)
    options.skeletal_mesh_import_data.set_editor_property('normal_import_method',unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)

    # unreal.FbxMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxSkeletalMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
    options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
    return options


def buildAnimationImportOptions(skeleton_path=''):
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.skeleton = unreal.load_asset(skeleton_path)
    options.set_editor_property('import_animations', True)
    options.set_editor_property("automated_import_should_detect_type", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    # unreal.FbxMeshImportData
    options.anim_sequence_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxAnimSequenceImportData
    options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    options.anim_sequence_import_data.set_editor_property('remove_redundant_keys', False)
    return options


def buildAbcImportOptions(frame_start, frame_end):
    options = unreal.AbcImportSettings()
    gc_settings = unreal.AbcGeometryCacheSettings()
    conversion_settings = unreal.AbcConversionSettings()
    sampling_settings = unreal.AbcSamplingSettings()
    options.set_editor_property('import_type', unreal.AlembicImportType.GEOMETRY_CACHE)
    # options.set_editor_property("import_type", unreal.AlembicImportType.SKELETAL)

    options.material_settings.set_editor_property("create_materials", False)
    options.material_settings.set_editor_property("find_materials", True)
    gc_settings.set_editor_property('flatten_tracks', True)
    conversion_settings.set_editor_property('flip_u', False)
    conversion_settings.set_editor_property('flip_v', True)
    conversion_settings.set_editor_property('scale', unreal.Vector(x=1, y=-1, z=1))
    conversion_settings.set_editor_property('rotation', unreal.Vector(x=90.0, y=0.0, z=0.0))
    sampling_settings.set_editor_property('frame_start', frame_start)
    sampling_settings.set_editor_property('frame_end', frame_end)
    options.geometry_cache_settings = gc_settings
    options.conversion_settings = conversion_settings
    options.sampling_settings = sampling_settings
    return options


def import_textures(texture_path,unreal_texture_path):
    import_texture_paths = []
    texture_names = []
    for root, dirnames, filenames in os.walk(texture_path):
        for filename in fnmatch.filter(filenames, '*.tga'):
            import_texture_paths.append((root, filename))
    import_tasks = []
    for import_texture_dir, import_texture_name in import_texture_paths:
        import_texture_path = os.path.join(import_texture_dir, import_texture_name)
        texture_name = import_texture_name.replace(".tga", "")
        texture_names.append(os.path.join(unreal_texture_path, texture_name))
        task = buildImportTask(import_texture_path,unreal_texture_path)
        import_tasks.append(task)
    executeImportTasks(import_tasks)
    return(texture_names)


def reimport_asset(asset_path):
    #Return Object(child of _ObjectBase) Class
    asset = unreal.EditorAssetLibrary.load_asset(asset_path) 
    import_data = asset.get_editor_property("asset_import_data")
    #Get fbx path, Ex: 'e:\dev\Player\Animation\Export\PE\A_Pl_Base_005.fbx'
    fbx_file_path = import_data.get_first_filename()
    import_task = unreal.AssetImportTask()
    #Important! Need to assgin fbx path to filename. 
    import_task.filename = fbx_file_path 
    #get_name() is a class method in _ObjectBase Class
    import_task.destination_name = asset.get_name() 
    import_task.destination_path = asset.get_path_name().rpartition("/")[0]
    #Ignore pop-up window
    import_task.replace_existing = True 
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([import_task])






# Cpp ###########################################################
# return: str List : The asset paths that are currently selected
def getSelectedAssets():
    return unreal.CppLib.get_selected_assets()


def setSelectedAssets(asset_paths=[]):
    unreal.CppLib.set_selected_assets(asset_paths)


def getSelectedFolders():
    return unreal.CppLib.get_selected_folders()


def setSelectedFolders(folder_paths=[]):
    unreal.CppLib.set_selected_folders(folder_paths)


def getAllOpenedAssets():
    return unreal.CppLib.get_assets_opened_in_editor()


def closeAssets(asset_objects=[]):
    unreal.CppLib.close_editor_for_assets(asset_objects)


def setDirectoryColor(path='', color=None):
    unreal.CppLib.set_folder_color(path, color)


def get_all_properties(options):
    object_class = options.get_class()
    for x in unreal.CppLib.get_all_properties(object_class):
        y = x
        while len(y) < 30:
            y = ' ' + y
        print (y + ' : ' + str(options.get_editor_property(x)))



# return: int : The index of the active viewport
def getActiveViewportIndex():
    return unreal.CppLib.get_active_viewport_index()

# viewport_index: int : The index of the viewport you want to affect
# location: obj unreal.Vector : The viewport location
# rotation: obj unreal.Rotator : The viewport rotation
def setViewportLocationAndRotation(viewport_index=1, location=unreal.Vector(), rotation=unreal.Rotator()):
    unreal.CppLib.set_viewport_location_and_rotation(viewport_index, location, rotation)

def executeConsoleCommand(console_command=''):
    world = ue_system.get_editor_world()
    unreal.SystemLibrary.execute_console_command(world,console_command)

def focusViewportOnActor(active_viewport_only=True, actor=None):
    command = 'CAMERA ALIGN'
    if active_viewport_only:
        command += ' ACTIVEVIEWPORTONLY'
    if actor:
        command += ' NAME=' + actor.get_name()
    executeConsoleCommand(command)


def test ():
    print("test")



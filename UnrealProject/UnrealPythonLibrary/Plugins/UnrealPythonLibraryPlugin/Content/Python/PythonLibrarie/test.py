import fnmatch
import os
import re
import sys
import json
import unreal
import importlib
print(unreal)
print("unreal")
import sys
sys.path.append(r"D:\program\UnrealPythonLibrary\UnrealProject\UnrealPythonLibrary\Plugins\UnrealPythonLibraryPlugin\Content\Python\PythonLibrarie")
import AssetFunctions
importlib.reload(AssetFunctions)
AssetFunctions.test()


ea_system = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ls_system = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
eu_system = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
ue_system = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
eas_system = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
le_system = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)


source_animation = unreal.load_asset('/Game/seq001/shot001/sq0010_anim_roudunplus01')
out_path = os.path.split(eas_system.get_path_name_for_loaded_asset(source_animation))[0]
create_pose_from_animation = unreal.CppLib.create_pose_from_animation(source_animation,["tets","test2"])
print(create_pose_from_animation)




current_level = le_system.get_current_level()
world = ue_system.get_editor_world()
unreal.SystemLibrary.execute_console_command(world,"CAMERA ALIGN ACTIVEVIEWPORTONLY")
unreal.PythonScriptLibrary.execute_python_command
unreal.CppLib.execute_console_command("CAMERA ALIGN ACTIVEVIEWPORTONLY")
unreal.CppLib.world_create_folder("/dddd/dddsss/ss")


animation_blueprint = unreal.load_asset('/Game/MetaHumans/Common/Female/Medium/NormalWeight/Body/f_med_nrw_animbp.f_med_nrw_animbp')

animation_graphs = animation_blueprint.get_animation_graphs()
animation_graphs = animation_blueprint.get_nodes_of_class()

print(dir(animation_graphs))



unreal.PoseDriverConnect.import_pose_drivers_from_json






ea_system.clear_actor_selection_set()
ea_system.set_selected_level_actors([])

print(ea_system.get_selected_level_actors())
le_system.save_current_level()
le_system.save_all_dirty_levels()


asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
asset_data = asset_registry.get_asset_by_object_path('/Game/seq001/shot001/sq0010_anim_jufubingplus')



asset_name = '/Game/seq001/shot001/sq0010_anim_jufubingplus'

asset_data = unreal.EditorAssetLibrary().find_asset_data(asset_name)
asset = asset_data.get_asset()

print(asset.get_path_name())

print(dir(asset))





# get level selected assets
world = ue_system.get_editor_world()
selected_actors = ea_system.get_selected_level_actors()
for actor in selected_actors:
    actor_name = actor.get_actor_label()
    print("选中的物体：", actor_name)


# get selected assets
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
for asset in selected_assets:
    AssetFunctions.get_all_properties(asset)


assets = AssetFunctions.getAllActors()
print(assets)






# import skeletal meshes
skeletal_mesh_task = AssetFunctions.buildImportTask(r"D:\p4\UE5Pipeline\D_PV_project\maya\assets\chr\H20030\H20030.rig.body\H20030_ue.fbx",
                                      '/Game/SkeletalMeshes/test', 
                                      AssetFunctions.buildSkeletalMeshImportOptions())
AssetFunctions.executeImportTasks([skeletal_mesh_task])

# import anim
animation_task = AssetFunctions.buildImportTask(r"D:\p4\UE5Pipeline\D_PV_project\maya\seq001\Shot_001\fbx\S001_H20030_ani_01.fbx", 
                                                '/Game/SkeletalMeshes/test',
                                                  AssetFunctions.buildAnimationImportOptions('/Game/SkeletalMeshes/test/H20030_ue_Skeleton'))
AssetFunctions.executeImportTasks([animation_task])

# import texture
texture_task = AssetFunctions.buildImportTask(r"D:\p4\UE5Pipeline\D_PV_project\maya\seq001\Shot_001\fbx\H20030_Body_HD_D.tga",
                                      '/Game/SkeletalMeshes/test')
AssetFunctions.executeImportTasks([texture_task])


# import textures 
texture_path = r"D:\p4\UE5Pipeline\D_PV_project\maya\assets\chr\H20030\H20030.rig.body\images"
unreal_texture_path = '/Game/SkeletalMeshes/test/textures'
AssetFunctions.import_textures(texture_path,unreal_texture_path)


# import skeletal meshes
abc_task = AssetFunctions.buildImportTask(r"D:\ue\shitou_abc.abc",
                                      '/Game/SkeletalMeshes/test', 
                                      AssetFunctions.buildAbcImportOptions(1,100))
AssetFunctions.executeImportTasks([abc_task])


# save all 
asset_dir = '/Game/SkeletalMeshes/test/textures'
asset_content = unreal.EditorAssetLibrary.list_assets(asset_dir, recursive=True, include_folder=True)
for a in asset_content:
    unreal.EditorAssetLibrary.save_asset(a)



# make dir
content_path = '/Game/SkeletalMeshes/test/textures'
if not unreal.EditorAssetLibrary.does_directory_exist(content_path):
    unreal.EditorAssetLibrary.make_directory(content_path)

unreal.EditorAssetLibrary.save_directory(f"/Game/{content_path}/", False)


# make dir
unreal.EditorLevelLibrary.new_level(f'/Game/{self.content_path}/map_{self.config["MeshName"]}')

unreal.EditorAssetLibrary.list_assets(f'/Game/{self.content_path}/Statics/', recursive=False)

# quat = unreal.Quat(instance["Rotation"][0], instance["Rotation"][1], instance["Rotation"][2], instance["Rotation"][3])
# euler = quat.euler()
# rotator = unreal.Rotator(-euler.x+180, -euler.y+180, -euler.z)
# location = [-instance["Translation"][0]*100, instance["Translation"][1]*100, instance["Translation"][2]*100]
unreal.EditorLevelLibrary.spawn_actor_from_object(sm,location=[0, 0, 0])

# save current level
unreal.EditorLevelLibrary.save_current_level()

unreal.EditorLevelLibrary.save_all_dirty_levels()






def assign_map_materials(self) -> None:
    for x in unreal.EditorAssetLibrary.list_assets(f'/Game/{self.content_path}/Statics/', recursive=False):
        # Identify static mesh
        mesh = unreal.load_asset(x)
        # Check material slots and compare names from config
        mesh_materials = mesh.get_editor_property("static_materials")
        material_slot_name_dict = {x: unreal.load_asset(f"/Game/{self.config['UnrealInteropPath']}/Materials/M_{y}") for x, y in self.config["Parts"].items()}
        new_mesh_materials = []
        for skeletal_material in mesh_materials:
            slot_name = skeletal_material.get_editor_property("material_slot_name").__str__()
            slot_name = '_'.join(slot_name.split('_')[:-1])
            if slot_name in material_slot_name_dict.keys():
                if material_slot_name_dict[slot_name] != None:
                    skeletal_material.set_editor_property("material_interface", material_slot_name_dict[slot_name])
            new_mesh_materials.append(skeletal_material)
        print(new_mesh_materials)
        mesh.set_editor_property("static_materials", new_mesh_materials)



def assign_entity_materials(self) -> None:
    # Identify entity mesh
    mesh = unreal.load_asset(f"/Game/{self.content_path}/{self.config['MeshName']}")
    # Check material slots and compare names from config
    mesh_materials = mesh.get_editor_property("materials")
    material_slot_name_dict = {x: unreal.load_asset(f"/Game/{self.config['UnrealInteropPath']}/Materials/M_{y}") for x, y in self.config["Parts"].items()}
    new_mesh_materials = []
    for skeletal_material in mesh_materials:
        slot_name = skeletal_material.get_editor_property("material_slot_name").__str__()
        slot_name = '_'.join(slot_name.split('_')[:-1])
        if slot_name in material_slot_name_dict.keys():
            if material_slot_name_dict[slot_name] != None:
                skeletal_material.set_editor_property("material_interface", material_slot_name_dict[slot_name])
        new_mesh_materials.append(skeletal_material)
    print(new_mesh_materials)
    mesh.set_editor_property("materials", new_mesh_materials)


def set_texture(material_instance, texture_name, texture_dir):
    texture_path = texture_dir + "/" + texture_name
    if unreal.EditorAssetLibrary.does_asset_exist(texture_path):
        texture = unreal.EditorAssetLibrary.load_asset(texture_path)
        parameter_name = ""
        if "color" in texture_name:
            parameter_name = "Color"
        elif "normal" in texture_name:
            parameter_name = "Normal"
        elif "specular" in texture_name:
            parameter_name = "Specular"
        else:
            unreal.log_error("Unknown texture extension: " + texture_name)
            return None
        unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, parameter_name, texture)
        return texture
    else:
        unreal.log_error("Texture not found")
        return None
    return



# make material
master_material_path = '/Game/Material/M_Rocketbox_Master'
master_material = unreal.EditorAssetLibrary.load_asset("Material'%s'" % master_material_path)
material_instance = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name="Material", 
                                                                            package_path="/Game/Material", 
                                                                            asset_class=unreal.MaterialInstanceConstant, 
                                                                            factory=unreal.MaterialInstanceConstantFactoryNew())
unreal.MaterialEditingLibrary.set_material_instance_parent(material_instance, master_material)
if unreal.EditorAssetLibrary.does_asset_exist(texture_path):
    texture = unreal.EditorAssetLibrary.load_asset(texture_path)
    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, "Color", texture)
unreal.EditorAssetLibrary.save_loaded_asset(material_instance)


# set static materials
material = unreal.load_asset('/Game/Megascans/3D_Assets/Fallen_Tree_Log_xiclbgu/MI_Fallen_Tree_Log_xiclbgu_2K')
mesh = unreal.load_asset('/Game/Megascans/3D_Assets/Fallen_Tree_Log_xiclbgu/S_Fallen_Tree_Log_xiclbgu_lod3_Var1')
mesh_materials = mesh.get_editor_property("static_materials")
new_mesh_materials = []
for skeletal_material in mesh_materials:
    skeletal_material.set_editor_property("material_interface", material)
    new_mesh_materials.append(skeletal_material)
mesh.set_editor_property("static_materials", new_mesh_materials)
unreal.EditorAssetLibrary.save_loaded_asset(mesh)


# set skelekal materials
material = unreal.load_asset('/Game/Characters/Mannequins/Materials/Instances/Manny/MI_Manny_01')
mesh = unreal.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple')

mesh_materials = mesh.get_editor_property("materials")
new_mesh_materials = []
for skeletal_material in mesh_materials:
    skeletal_material.set_editor_property("material_interface", material)
    new_mesh_materials.append(skeletal_material)
mesh.set_editor_property("materials", new_mesh_materials)
unreal.EditorAssetLibrary.save_loaded_asset(mesh)




# 当前 Map 打开 sequence
level_sequence = unreal.load_asset('/Game/Test_level')
# level_sequence = unreal.load_asset('/Game/TK/env')
print(level_sequence)
unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(level_sequence)



# Get Current Sequence
level_sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
print(level_sequence)


# Create New Sequence
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name = "Test_LS", package_path = "/Game/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(level_sequence)


# Set Frame Rate
frame_rate = unreal.FrameRate(numerator = 30, denominator = 1)
level_sequence.set_display_rate(frame_rate)

# Set Start End Frame
level_sequence.set_playback_start(1)
level_sequence.set_playback_end(22)


level_sequence.set_view_range_start(float)
level_sequence.set_view_range_end(float)

level_sequence.set_work_range_start(float)
level_sequence.set_work_range_end(float)

unreal.LevelSequenceEditorBlueprintLibrary.set_current_time(1)





# add actor to sequence
actor = unreal.EditorLevelLibrary.get_selected_level_actors()[0]
actor_binding = level_sequence.add_possessable(actor)
spawn_track = actor_binding.add_track(unreal.MovieSceneSpawnTrack)
spawn_track.add_section()
print(actor_binding.get_tracks()[0].get_display_name())
print(actor_binding.get_display_name())


# add actor spawnable to sequence
actor_binding = level_sequence.add_spawnable_from_instance(actor)
print(dir(actor_binding))

# refresh
unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

# add transform tranck
transform_track = actor_binding.add_track(unreal.MovieScene3DTransformTrack)
transform_section = transform_track.add_section() 

# add anim tranck
anim_track = actor_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
anim_section = anim_track.add_section()


start_frame = level_sequence.get_playback_start()
end_frame = level_sequence.get_playback_end()
print(start_frame,end_frame)
transform_section.set_range(start_frame, end_frame)
anim_section.set_range(start_frame, end_frame)



# test 
tk = unreal.load_asset('/Game/Characters/TK/TLZ_TK_rig_hiRes')
print(tk)
actor_binding = level_sequence.add_spawnable_from_instance(tk)
anim_track = actor_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
anim_section = anim_track.add_section()
print(help(anim_track))
anim_seq = unreal.load_asset('/Game/Characters/TK/anim/TK_anim')
anim_section.params.animation = anim_seq
anim_section.set_range(start_frame, end_frame)


time_range = anim_seq.get_play_length()
print(time_range)



anim_asset_path = '/Game/Characters/TK/anim/TK_anim'
anim_asset_path = '/Game/Characters/Mannequins/Animations/Manny/MM_Fall_Loop'

animation_asset = unreal.EditorAssetLibrary.load_asset(anim_asset_path)  
anim_seq = unreal.load_asset(anim_asset_path)
print(animation_asset,anim_seq)

number_of_sampled_keys = anim_seq.get_editor_property("number_of_sampled_keys")
frame_rate = anim_seq.get_editor_property('target_frame_rate')
print(number_of_sampled_keys)
print(frame_rate.numerator)





anim_asset_paths = '/Game/Characters/Mannequins/Animations/Manny'
assets = unreal.EditorAssetLibrary.list_assets(anim_asset_paths)
for asset in assets:
    anim = unreal.load_asset(asset)
    # get anim asset path
    directory = unreal.Paths.get_path(anim.get_path_name())
    print(directory)
    frame_count = unreal.AnimationLibrary.get_num_frames(anim)
    print(frame_count)


# get select assets
anim_seq = unreal.EditorUtilityLibrary.get_selected_assets()[0]
print(anim_seq.get_name())


rig_actor = unreal.EditorLevelLibrary.get_selected_level_actors()[0]
sequencer = unreal.EditorUtilityLibrary.get_selected_assets()[0]

# 将actor添加到level sequencer中
possessable = sequencer.add_possessable(rig_actor)

# 添加 Transform track
transform_track = possessable.add_track(track_type=unreal.MovieScene3DTransformTrack)

# 添加 section
transform_section = transform_track.add_section()
transform_section.set_range(1, 120)

# 创建track和section
ani_track = possessable.add_track(track_type=unreal.MovieSceneSkeletalAnimationTrack)  
ani_section = ani_track.add_section()

# 获取选中的动画资产
ani_asset = unreal.EditorUtilityLibrary.get_selected_assets()[0]

# 实例化params对象
params = unreal.MovieSceneSkeletalAnimationParams()  
params.set_editor_property('Animation', ani_asset)

# 添加asset资产，修改时间范围
ani_section.set_editor_property('Params', params)
ani_section.set_range(1, 120)







# get source file
fbx_path = anim_seq.get_editor_property("asset_import_data").get_first_filename()
print(fbx_path)
print(dir(fbx_path))

# get source files
fbx_path = anim_seq.get_editor_property("asset_import_data").extract_filenames()
print(fbx_path)


fbx_path = anim_seq.get_editor_property("asset_import_data")
print(fbx_path)


asset_import_data = anim_seq.get_editor_property("asset_import_data")
print(anim_seq,asset_import_data)


asset_import_data = anim_seq.get_editor_property("asset_import_data").get_editor_property("source_data")
print(dir(asset_import_data))

print(help(asset_import_data))

# AnimSequence FbxAnimSequenceImportData
get_all_properties(anim_seq)






cache_asset = unreal.load_asset('/Game/TK/PP')
# add asset to scence
cache_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(cache_asset,unreal.Vector(x=0.0, y=0.0, z=0.0))
actor_binding = level_sequence.add_spawnable_from_instance(cache_actor)


# adding a geom cache
cache_track = actor_binding.add_track(unreal.MovieSceneGeometryCacheTrack)
anim_section = cache_track.add_section()
anim_section.set_range(start_frame,end_frame) # start and end frames


# add the cache asset 
params = anim_section.get_editor_property("params")
params.set_editor_property("geometry_cache_asset",cache_asset)
unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()


# sequence 套娃
master_track = level_sequence.add_master_track(unreal.MovieSceneSubTrack)
subseq = unreal.load_asset("/Game/path/to/subsequence" )
subsequence_section = master_track.add_section()
subsequence_section.set_sequence(subseq)
subsequence_section.set_range(start_frame,end_frame)


# reimport asset
asset_path ='/Game/Characters/roudunplus/roudunplus'
AssetFunctions.reimport_asset(asset_path)




unreal.EditorLevelLibrary.save_current_level()

current_level = le_system.get_current_level()
world = ue_system.get_editor_world()



sequences_name = "leishen"
level_sequence_path = f'/Game/Cinematics/Sequences/Sequence/{sequences_name}'
# level_sequence_path = '/Game/Test_level'
package_path,asset_name = os.path.split(level_sequence_path)
if AssetFunctions.assetExist(level_sequence_path):
    level_sequence = unreal.load_asset(level_sequence_path)
else:
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name = asset_name, 
                                                    package_path = package_path, 
                                                    asset_class = unreal.LevelSequence, 
                                                    factory = unreal.LevelSequenceFactoryNew())



levelSequenceActors = AssetFunctions.getAllActors(actor_class=unreal.LevelSequenceActor)
if levelSequenceActors:
    for a in levelSequenceActors:
        if a.get_actor_label() == asset_name:
            levelSequenceActor = a
            break
else:
    levelSequenceActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.LevelSequenceActor, unreal.Vector())
    levelSequenceActor.set_actor_label(asset_name)  
    levelSequenceActor.set_sequence(level_sequence)



unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(level_sequence)
level_sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
print(level_sequence)



json_file_path = r"D:\projects\zbgame\work\shot\seq\lenshen\ani\lenshen.ani.001\export_asset.json"
with open(json_file_path, "r") as json_file:
    sequence_data = json.load(json_file)
root_path = os.path.split(json_file_path)[0]
char_folder = level_sequence.add_root_folder_to_sequence("char")
print(char_folder)


camera = sequence_data['camera'][0]
print(camera)
start_frame,end_frame = sequence_data['frame_range']
print(start_frame,end_frame)
fbxs = sequence_data['fbx']
animation_tasks = []
actor_bindings = []
frame_rate = unreal.FrameRate(numerator = 30, denominator = 1)
level_sequence.set_display_rate(frame_rate)

# Set Start End Frame
level_sequence.set_playback_start(start_frame)
level_sequence.set_playback_end(end_frame)

for fbx in fbxs.keys():
    fbx_file = fbxs[fbx]
    skeleton_file_path = f'/Game/Characters/{fbx_file}/{fbx_file}_Skeleton'
    char_file_path = f'/Game/Characters/{fbx_file}/{fbx_file}'
    actor_binding = level_sequence.add_spawnable_from_instance(unreal.load_asset(char_file_path))
    actor_binding.set_display_name(fbx)
    actor_binding.set_name(fbx)
    char_folder.add_child_object_binding(actor_binding)
    ani_fbx_path = f'{root_path}/fbx/{fbx}.fbx'
    print(ani_fbx_path,skeleton_file_path)

    level_shot_path = f'/Game/Cinematics/Sequences/{sequences_name}'
    animation_task = AssetFunctions.buildImportTask(ani_fbx_path, level_shot_path,
                                                  AssetFunctions.buildAnimationImportOptions(skeleton_file_path))
    animation_tasks.append(animation_task)
    actor_bindings.append(actor_binding)

imported_asset_paths = AssetFunctions.executeImportTasks(animation_tasks)

for imported_asset_path,actor_binding in zip(imported_asset_paths,actor_bindings):
    anim_track = actor_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
    anim_section = anim_track.add_section()
    anim_seq = unreal.load_asset(imported_asset_path)
    anim_section.params.animation = anim_seq
    anim_section.set_range(start_frame, end_frame)


# make camera 
# level_sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
camera_folder = level_sequence.add_root_folder_to_sequence("camera")
camera_binding = level_sequence.add_spawnable_from_class(unreal.CineCameraActor)
camera_folder.add_child_object_binding(camera_binding)
transform_track = camera_binding.add_track(unreal.MovieScene3DTransformTrack)
transform_section = transform_track.add_section()
transform_section.set_start_frame_bounded(0)
transform_section.set_end_frame_bounded(0)
camera_binding.set_display_name('ShotCam')
camera_binding.set_name('ShotCam')

# add a camera cut track
camera_cut_track = level_sequence.add_track(unreal.MovieSceneCameraCutTrack)
camera_cut_section = camera_cut_track.add_section()
# camera_cut_section.set_start_frame_seconds(101)
# camera_cut_section.set_end_frame_seconds(230)
camera_cut_section.set_start_frame_bounded(0)
camera_cut_section.set_end_frame_bounded(0)
camera_cut_section.set_range(start_frame, end_frame)

# add the binding for the camera cut section
camera_binding_id = level_sequence.make_binding_id(camera_binding, unreal.MovieSceneObjectBindingSpace.LOCAL)
camera_cut_section.set_camera_binding_id(camera_binding_id)


# import camera animation
import_setting = unreal.MovieSceneUserImportFBXSettings()  
import_setting.set_editor_property('create_cameras', False)  
import_setting.set_editor_property('force_front_x_axis', False)  
import_setting.set_editor_property('match_by_name_only', False)  
import_setting.set_editor_property('reduce_keys', False)
import_setting.set_editor_property('reduce_keys_tolerance', 0.001)
world = ue_system.get_editor_world()  
unreal.SequencerTools.import_level_sequence_fbx(world, level_sequence, [camera_binding], import_setting, f'{root_path}/fbx/{camera}.fbx')
unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()


#######################
# edit camera settings
#######################
world = ue_system.get_editor_world()  
actor_list = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.CineCameraActor)
for actor in actor_list:
    camera_component = actor.get_cine_camera_component()
    print(camera_component)
    # camera_component.focus_settings.set_editor_property("focus_method", unreal.CameraFocusMethod.DISABLE)
    _focusSettings = unreal.CameraFocusSettings()
    _focusSettings.manual_focus_distance = 1320.0
    _focusSettings.focus_method = unreal.CameraFocusMethod.DISABLE
    _focusSettings.focus_offset = 19.0
    _focusSettings.smooth_focus_changes = False
    camera_component.set_editor_property("focus_settings", _focusSettings)

unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()
le_system.save_current_level()
# unreal.EditorAssetLibrary.save_asset(level_sequence_path)
unreal.EditorAssetLibrary.save_loaded_asset(level_sequence)




#######################
# 先设置后转换spawnable
#######################
ls_system = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
cine_camera = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor, unreal.Vector())
cine_camera.set_actor_label('ShotCam')  
binding = level_sequence.add_possessable(cine_camera)  
cine_camera_binding = level_sequence.add_possessable(cine_camera.get_cine_camera_component())

_cineCameraComponent = cine_camera.get_cine_camera_component()
print(cine_camera)
_focusSettings = unreal.CameraFocusSettings()
_focusSettings.manual_focus_distance = 1320.0
_focusSettings.focus_method = unreal.CameraFocusMethod.DISABLE
_focusSettings.focus_offset = 19.0
_focusSettings.smooth_focus_changes = False
_cineCameraComponent.set_editor_property("focus_settings", _focusSettings)

ls_system.convert_to_spawnable(binding)
unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()



level_sequence = unreal.load_asset('/Game/NewLevelSequence.NewLevelSequence')
# unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(level_sequence)
# level_sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
for binding in level_sequence.get_bindings():
    # print(binding.get_name())
    if binding.get_name() == "Cine Camera Actor":
        bound_objects = unreal.SequencerTools.get_bound_objects(ue_system.get_editor_world(),
                                                                level_sequence,[binding],unreal.SequencerScriptingRange(
                                                                    has_start_value=True,
                                                                    has_end_value=True,
                                                                    inclusive_start=level_sequence.get_playback_start(),
                                                                    exclusive_end=level_sequence.get_playback_end()
                                                                ))
        cine_camera = binding.get_object_template()
        _cineCameraComponent = cine_camera.get_editor_property("camera_component")
        print(_cineCameraComponent)
        _focusSettings = unreal.CameraFocusSettings()
        _focusSettings.manual_focus_distance = 1320.0
        _focusSettings.focus_method = unreal.CameraFocusMethod.DISABLE
        _focusSettings.focus_offset = 19.0
        _focusSettings.smooth_focus_changes = False
        _cineCameraComponent.set_editor_property("focus_settings", _focusSettings)
unreal.EditorAssetLibrary.save_loaded_asset(level_sequence)






# Import built-in modules
from collections import defaultdict
import json
import os

# Import local modules
import unreal

DIR = os.path.dirname(os.path.abspath(__file__))

def unreal_progress(tasks, label="进度", total=None):
    total = total if total else len(tasks)
    with unreal.ScopedSlowTask(total, label) as task:
        task.make_dialog(True)
        for i, item in enumerate(tasks):
            if task.should_cancel():
                break
            task.enter_progress_frame(1, "%s %s/%s" % (label, i, total))
            yield item


def main():
    # NOTE: 读取 sequence
    sequence = unreal.load_asset('/Game/Sequencer/MetaHumanSample_Sequence.MetaHumanSample_Sequence')
    # NOTE: 收集 sequence 里面所有的 binding
    binding_dict = defaultdict(list)
    for binding in sequence.get_bindings():
        binding_dict[binding.get_name()].append(binding)

    # NOTE: 遍历命名为 Face 的 binding
    for binding in unreal_progress(binding_dict.get("Face", []), "导出 Face 数据"):
        # NOTE: 获取关键帧 channel 数据
        keys_dict = {}
        for track in binding.get_tracks():
            for section in track.get_sections():
                for channel in unreal_progress(section.get_channels(), "导出关键帧"):
                    if not channel.get_num_keys():
                        continue
                    keys = []
                    for key in channel.get_keys():
                        frame_time = key.get_time()
                        frame = frame_time.frame_number.value + frame_time.sub_frame
                        keys.append({"frame": frame, "value": key.get_value()})

                    keys_dict[channel.get_name()] = keys

        # NOTE: 导出 json
        name = binding.get_parent().get_name()
        export_path = os.path.join(DIR, "{0}.json".format(name))
        with open(export_path, "w") as wf:
            json.dump(keys_dict, wf, indent=4)















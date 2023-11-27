#include "CppLib.h"
#include "Runtime/Core/Public/Misc/ConfigCacheIni.h"
//PublicDependencyModuleNames-> "UnrealEd"
#include "Editor/UnrealEd/Public/Editor.h" 
#include "Editor/UnrealEd/Public/LevelEditorViewport.h"
// PublicDependencyModuleNames -> "ContentBrowser"
#include "Editor/ContentBrowser/Public/ContentBrowserModule.h"
#include "Editor/ContentBrowser/Private/SContentBrowser.h"
#include "Subsystems/AssetEditorSubsystem.h"
// PublicDependencyModuleNames -> "AssetRegistry"
#include "Runtime/AssetRegistry/Public/AssetRegistryModule.h"
// PublicDependencyModuleNames -> "PythonScriptPlugin" && "Python"
// #include "../Plugins/Experimental/PythonScriptPlugin/Source/PythonScriptPlugin/Private/PythonScriptPlugin.h"
#include "UObject/Class.h"
#include "UObject/PropertyPortFlags.h"
#include "UObject/Package.h"
#include "Misc/FileHelper.h"
#include "EditorFramework/AssetImportData.h"
#include "Editor/UnrealEd/Public/EditorActorFolders.h"
//PublicDependencyModuleNames-> "UnrealEd"
#include "AssetRegistry/AssetData.h"
#include "Engine/ObjectLibrary.h"
#include "Subsystems/EditorAssetSubsystem.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "Editor/EditorEngine.h" // GEditor Í·ÎÄ¼þ
#include "Editor.h" 
#include "ActorFolder.h"
#include "WorldPersistentFolders.h"
#include "ActorEditorUtils.h"
#include "Animation/Skeleton.h"
#include "Animation/AnimSequence.h"
#include "Animation/PoseAsset.h"

#include "Factories/PoseAssetFactory.h"
#include "IContentBrowserSingleton.h"
#include "ContentBrowserModule.h"
#include "AssetRegistryModule.h"
#include "PackageTools.h"
#include "Misc/Paths.h"

TArray<FString> UCppLib::GetAllProperties(UClass* Class) {
	TArray<FString> Ret;
	if (Class != nullptr) {
		for (TFieldIterator<FProperty> It(Class); It; ++It) {
			FProperty* Property = *It;
			if (Property->HasAnyPropertyFlags(EPropertyFlags::CPF_Edit)) {
				Ret.Add(Property->GetName());
			}
		}
	}
	return Ret;
}

void UCppLib::ExecuteConsoleCommand(FString ConsoleCommand) {
	if (GEditor) {
		UWorld* World = GEditor->GetEditorWorldContext().World();
		if (World) {
			GEditor->Exec(World, *ConsoleCommand, *GLog);
		}
	}
}

TArray<FString> UCppLib::GetSelectedAssets() {
	FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	TArray<FAssetData> SelectedAssets;
	ContentBrowserModule.Get().GetSelectedAssets(SelectedAssets);
	TArray<FString> Result;
	for (FAssetData& AssetData : SelectedAssets) {
		Result.Add(AssetData.PackageName.ToString());
	}
	return Result;
}

void UCppLib::SetSelectedAssets(TArray<FString> Paths) {
	FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry");
	TArray<FName> PathsName;
	for (FString Path : Paths) {
		PathsName.Add(*Path);
	}
	FARFilter AssetFilter;
	AssetFilter.PackageNames = PathsName;
	TArray<FAssetData> AssetDatas;
	AssetRegistryModule.Get().GetAssets(AssetFilter, AssetDatas);
	ContentBrowserModule.Get().SyncBrowserToAssets(AssetDatas);
}

TArray<FString> UCppLib::GetSelectedFolders() {
	FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	TArray<FString> SelectedFolders;
	ContentBrowserModule.Get().GetSelectedFolders(SelectedFolders);
	return SelectedFolders;
}

void UCppLib::SetSelectedFolders(TArray<FString> Paths) {
	FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	ContentBrowserModule.Get().SyncBrowserToFolders(Paths);
}

void UCppLib::CloseEditorForAssets(TArray<UObject*> Assets) {
	UAssetEditorSubsystem* AssetEditorSubsystem = GEditor->GetEditorSubsystem<UAssetEditorSubsystem>();

	for (UObject* Asset : Assets) {
		AssetEditorSubsystem->CloseAllEditorsForAsset(Asset);
	}
}

TArray<UObject*> UCppLib::GetAssetsOpenedInEditor() {
	TArray<UObject*> EditedAssets = GEditor->GetEditorSubsystem<UAssetEditorSubsystem>()->GetAllEditedAssets();

	return EditedAssets;
}

void UCppLib::SetFolderColor(FString FolderPath, FLinearColor Color) {
	GConfig->SetString(TEXT("PathColor"), *FolderPath, *Color.ToString(), GEditorPerProjectIni);
}

int UCppLib::GetActiveViewportIndex() {
	int Index = 1;
	if (GEditor != nullptr && GCurrentLevelEditingViewportClient != nullptr) {
		GEditor->GetLevelViewportClients().Find(GCurrentLevelEditingViewportClient, Index);
	}
	return Index;
}

// ViewportIndex is affected by the spawning order and not the viewport number. 
//    e.g. Viewport 4 can be the first one if the user spawned it first.
//         And can become the last one if the user open the other ones and then close and re-open Viewport 4.
//    Also, the indexes are confusing.
// 1st Spawned Viewport : Index = 1
// 2nd Spawned Viewport : Index = 5
// 3rd Spawned Viewport : Index = 9
// 4th Spawned Viewport : Index = 13
void UCppLib::SetViewportLocationAndRotation(int ViewportIndex, FVector Location, FRotator Rotation) {
	if (GEditor != nullptr && ViewportIndex < GEditor->GetLevelViewportClients().Num()) {
		FLevelEditorViewportClient* LevelViewportClient = GEditor->GetLevelViewportClients()[ViewportIndex];
		if (LevelViewportClient != nullptr) {
			LevelViewportClient->SetViewLocation(Location);
			LevelViewportClient->SetViewRotation(Rotation);
		}
	}
}

void UCppLib::WorldCreateFolder(FName path) {

	UWorld* world = GEditor->GetEditorWorldContext().World();
	// FFolder ParentFolder = FFolder::GetInvalidFolder();
	// const FFolder::FRootObject& RootObject = ParentFolder.GetRootObject();
	// FFolder DefaultFolderName = FActorFolders::Get().GetDefaultFolderName(*world, ParentFolder);
	// const FFolder NewFolderName = FActorFolders::Get().GetDefaultFolderForSelection(*world);
	// FFolder RootFolder = FFolder::GetWorldRootFolder(world);
	// FFolder NewFolderName(RootObject, FName("aaa/bbbb/tests1"));
	FActorFolders::Get().CreateFolder(*world, path);
}

void UCppLib::ExecutePythonScript(FString PythonScript) {
	//FPythonScriptPlugin::Get()->ExecPythonCommand(*PythonScript);
}
UPoseAsset* UCppLib::CreatePoseFromAnimation(UAnimSequence* SourceAnimation, TArray<FString> PoseNames) {

	FString AssetPath = FAssetData(SourceAnimation).GetExportTextName();
	FString animSequencePath = SourceAnimation->GetPathName();
	FString animSequenceParentPath = FPaths::GetPath(animSequencePath);
	// UE_LOG(LogTemp, Warning, TEXT("AnimSequence File Path: %s"), *animSequenceParentPath);

	if (SourceAnimation)
	{
		USkeleton* TargetSkeleton = SourceAnimation->GetSkeleton();
		TArray<FSmartName> InputPoseNames;
		if (PoseNames.Num() > 0)
		{
			for (int32 Index = 0; Index < PoseNames.Num(); ++Index)
			{
				FName PoseName = FName(*PoseNames[Index]);
				FSmartName NewName;
				if (TargetSkeleton->GetSmartNameByName(USkeleton::AnimCurveMappingName, PoseName, NewName) == false)
				{
					TargetSkeleton->AddSmartNameAndModify(USkeleton::AnimCurveMappingName, PoseName, NewName);
				}
				InputPoseNames.AddUnique(NewName);
			}
		}
		// FString(SourceAnimation->GetName())
		FString PackageName = UPackageTools::SanitizePackageName(*(animSequenceParentPath / FString(SourceAnimation->GetName())+"_pose"));
		UE_LOG(LogTemp, Warning, TEXT("AnimSequence File Path: %s"), *PackageName);
		//return nullptr;

		UPackage* Pkg = CreatePackage(*PackageName);
		EObjectFlags Flags = RF_Public | RF_Standalone | RF_Transactional;
		UPoseAsset* PoseAsset = NewObject<UPoseAsset>(Pkg, FName(*SourceAnimation->GetName()), Flags);
		PoseAsset->CreatePoseFromAnimation(SourceAnimation, &InputPoseNames);
		// PoseAsset->SetSkeleton(TargetSkeleton);
		PoseAsset->ConvertSpace(true, 0);
		return PoseAsset;
	}
	return nullptr;

}

int UCppLib::Test() {

	int Index = 1;
	return Index;
}


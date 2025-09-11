from typing import Final
from pathlib import Path
from shutil import copy2 as copy
from shutil import copytree
from shutil import rmtree
from os.path import isdir
from os.path import isfile
from subprocess import run

CfgFileValuesMapOfMap: dict[str, dict[str, str]] = {}

def main() -> None:
    project_root_folder_path: Path = Path(__file__).parents[3]
    build_folder_path: Path = project_root_folder_path / "build"

    does_build_folder_exist: Final[bool] = checkIfBuildFolderExists(build_folder_path)
    is_build_folder_empty: Final[bool] = checkIfBuildFolderIsEmpty(build_folder_path)

    if not does_build_folder_exist:
        print("[ERROR]: Build folder doesn't exist, please run build script first!")
        exit(1)
    elif is_build_folder_empty:
        print("[ERROR]: Build folder is empty, please run build script first!")
        exit(1)

    cfg_file_path: Final[Path] = Path(__file__).parents[1] / "cmake.conf"

    does_cfg_file_exist: Final[bool] = checkIfCfgFileExists(cfg_file_path)

    if not does_cfg_file_exist:
        print("[ERROR]: Cfg file doesn't exist, please run build script first!")
        exit(1)

    cfg_details: dict[str, str] = loadCfgDetailsFromFile(cfg_file_path)

    output_folder_path: Path = project_root_folder_path / "output"

    library_name: str = "gw_log_sys"
    headers_folder_path: Path = project_root_folder_path / "library" / "include"
    files_to_pack_paths: list[Path] = getFilePathsToPack(cfg_details, build_folder_path, library_name, headers_folder_path)

    buildOutputFolderIfNeeded(output_folder_path)

    target_folder_name: str = buildTargetFolderName(cfg_details)

    target_folder_path: Path = buildTargetFolder(output_folder_path, target_folder_name)

    copyFilesToTargetFolder(files_to_pack_paths, target_folder_path)

    compressTargetFolder(target_folder_path, target_folder_name)

    deleteTargetFolder(target_folder_path)

CfgFileValuesMapOfMap: dict[str, dict[str, str]] = {"Host platform": {"Linux": "Linux"},
                                                    "Toolchain": {"Ninja (gcc)": "Ninja (gcc)"},
                                                    "Target architecture": {"64-bit": "64-bit", "32-bit": "32-bit"},
                                                    "Build mode": {"Release": "Release", "Debug": "Debug"},
                                                    "Library type": {"Static": "Static", "Shared": "Shared"},
                                                    "Build tests status": {"Yes": "Yes", "No": "No"}}

def deleteTargetFolder(folder_path: Path) -> None:
    if folder_path.exists():
        rmtree(folder_path)

def compressTargetFolder(target_folder_path: Path, target_folder_name: str) -> None:
    tar_file_path: Path = target_folder_path.parent / f"{target_folder_name}.tar.gz"
    if tar_file_path.exists():
        tar_file_path.unlink()

    run(["tar", "-czf", str(tar_file_path), "-C", str(target_folder_path.parent), target_folder_name], check=True)

def copyFilesToTargetFolder(files_to_pack_list: list[Path], target_folder_path: Path) -> None:
    for file_path in files_to_pack_list:
        if isfile(file_path):
            copy(file_path, target_folder_path)
        elif isdir(file_path):
            copytree(file_path, target_folder_path / file_path.name, dirs_exist_ok=True)

def buildTargetFolder(output_folder_path: Path, target_folder_name: str) -> Path:
    target_folder_path: Path = output_folder_path / target_folder_name
    target_folder_path.mkdir(exist_ok=True)
    return target_folder_path

def buildTargetFolderName(cfg_details: dict[str, str]) -> str:
    target_folder_name: str = ""

    target_folder_name += "linux"

    if cfg_details["Target architecture"] == CfgFileValuesMapOfMap["Target architecture"]["64-bit"]:
        target_folder_name += "__64bit__"
    elif cfg_details["Target architecture"] == CfgFileValuesMapOfMap["Target architecture"]["32-bit"]:
        target_folder_name += "__32bit__"

    if cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Ninja (gcc)"]:
        target_folder_name += "ninja_gcc__"

    if cfg_details["Build mode"] == CfgFileValuesMapOfMap["Build mode"]["Release"]:
        target_folder_name += "release__"
    elif cfg_details["Build mode"] == CfgFileValuesMapOfMap["Build mode"]["Debug"]:
        target_folder_name += "debug__"

    if cfg_details["Library type"] == CfgFileValuesMapOfMap["Library type"]["Static"]:
        target_folder_name += "static"
    elif cfg_details["Library type"] == CfgFileValuesMapOfMap["Library type"]["Shared"]:
        target_folder_name += "shared"

    return target_folder_name

def buildOutputFolderIfNeeded(folder_path: Path) -> None:
    if not folder_path.exists():
        folder_path.mkdir()

def getFilePathsToPack(cfg_details: dict[str, str], build_folder_path: Path, library_name: str, headers_folder_path: Path) -> list[Path]:
    file_paths: list[Path] = []
    file_path: Path = Path()

    if cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Ninja (gcc)"]:
        if cfg_details["Library type"] == CfgFileValuesMapOfMap["Library type"]["Static"]:
            file_path = build_folder_path / f"{library_name}.a"
            file_paths.append(file_path)
        elif cfg_details["Library type"] == CfgFileValuesMapOfMap["Library type"]["Shared"]:
            file_path = build_folder_path / f"lib{library_name}.so"
            file_paths.append(file_path)

    file_paths.append(headers_folder_path)

    return file_paths

def loadCfgDetailsFromFile(file_path: Path) -> dict[str, str]:
    configuration: dict[str, str] = {
        "Host platform": "Linux",
        "Toolchain": "",
        "Target architecture": "",
        "Build mode": "",
        "Library type": "",
        "Build tests status": ""
    }

    segments_count_per_cfg_item: int = 3

    with open(file_path, "r") as file:
        line_index: int = 0
        cfg_item_index: int = 0
        current_header: str = ""

        for line in file:
            cfg_item_index = line_index % segments_count_per_cfg_item

            line = line.strip('\n')

            if cfg_item_index == 0:
                line = line.lstrip('[')
                line = line.rstrip(']')

                current_header = line
            elif cfg_item_index == 1:
                configuration[current_header] = line

            line_index += 1

    return configuration

def checkIfCfgFileExists(file_path: Path) -> bool:
    return file_path.exists()

def checkIfBuildFolderIsEmpty(folder_path: Path) -> bool:
    if folder_path.exists() and not any(folder_path.iterdir()):
        return True
    else:
        return False

def checkIfBuildFolderExists(folder_path: Path) -> bool:
    if folder_path.exists():
        return True
    else:
        return False

if __name__ == "__main__":
    main()

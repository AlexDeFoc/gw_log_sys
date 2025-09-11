from typing import Final
from pathlib import Path
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

    is_building_tests_true_in_cfg_details: bool = checkIfUserChooseToBuildTests(cfg_details)

    if not is_building_tests_true_in_cfg_details:
        print("[ERROR]: Cfg file says you didn't build tests, please run build script again and build tests!")
        exit(1)

    executable_name: str = "gw_log_sys_tests"
    runTests(cfg_details, build_folder_path, executable_name)

CfgFileValuesMapOfMap: dict[str, dict[str, str]] = {"Host platform": {"Linux": "Linux"},
                                                    "Toolchain": {"Ninja (gcc)": "Ninja (gcc)"},
                                                    "Target architecture": {"64-bit": "64-bit", "32-bit": "32-bit"},
                                                    "Build mode": {"Release": "Release", "Debug": "Debug"},
                                                    "Library type": {"Static": "Static", "Shared": "Shared"},
                                                    "Build tests status": {"Yes": "Yes", "No": "No"}}

def runTests(cfg_details: dict[str, str], build_folder_path: Path, executable_name: str) -> None:
    executable_path: Path = Path()

    if cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Ninja (gcc)"]:
        executable_path = build_folder_path / f"{executable_name}"

    run(executable_path)

def checkIfUserChooseToBuildTests(cfg_details: dict[str, str]) -> bool:
    if cfg_details["Build tests status"] == CfgFileValuesMapOfMap["Build tests status"]["Yes"]:
        return True
    else:
        return False

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

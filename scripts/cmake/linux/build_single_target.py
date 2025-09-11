from typing import Final
from pathlib import Path
from shutil import rmtree
from subprocess import run

CfgFileHeadersList: list[str] = []
CfgFileValuesMapOfLists: dict[str, list[str]] = {}
CfgFileValuesMapOfMap: dict[str, dict[str, str]] = {}

def main() -> None:
    cfg_file_path: Final[Path] = Path(__file__).parents[1] / "cmake.conf"

    does_cfg_file_exist: Final[bool] = checkIfCfgFileExists(cfg_file_path)

    cfg_details: dict[str, str] = {}

    should_rebuild_build_folder: bool = False
    build_folder_just_built: bool = False
    project_root_folder_path: Path = Path(__file__).parents[3]
    build_folder_path: Path = project_root_folder_path / "build"

    if does_cfg_file_exist == True:
        validateCfgFileContents(cfg_file_path)
    else:
        cfg_details = askUserForCfgDetails()
        createNewCfgFile(cfg_file_path, cfg_details)
        should_rebuild_build_folder = True

    if does_cfg_file_exist == True:
        user_wants_to_load_existing_cfg_file: bool = askUserIfTheyWantToLoadExistingCfgFile()

        if user_wants_to_load_existing_cfg_file:
            cfg_details = loadCfgDetailsFromFile(cfg_file_path)
            build_folder_just_built = makeSureFolderExists(build_folder_path)

            if not build_folder_just_built:
                build_folder_just_built = checkIfFolderExistsButItsIsEmpty(build_folder_path)
        else:
            cfg_details = askUserForCfgDetails()
            createNewCfgFile(cfg_file_path, cfg_details)
            should_rebuild_build_folder = True

        if user_wants_to_load_existing_cfg_file and not build_folder_just_built:
            user_wants_to_force_reconfigure_project: bool = askUserIfTheyWantToForceReconfigureProject()

            if user_wants_to_force_reconfigure_project:
                should_rebuild_build_folder = True

    if should_rebuild_build_folder:
        rebuildFolder(build_folder_path)

    cmake_file_folder_path: Path = project_root_folder_path
    cmake_configure_cmd: str = ""
    cmake_build_cmd: str = ""

    cmake_configure_cmd, cmake_build_cmd = buildCMakeCmds(cmake_file_folder_path, build_folder_path, cfg_details)

    if should_rebuild_build_folder or build_folder_just_built:
        runCMakeConfigureCmd(cmake_configure_cmd)

    runCMakeBuildCmd(cmake_build_cmd)

CfgFileHeadersList: list[str] =  ["Host platform", "Toolchain", "Target architecture", "Build mode", "Library type", "Build tests status"]

CfgFileValuesMapOfLists: dict[str, list[str]] = {"Host platform": ["Linux"],
                                                 "Toolchain": ["Ninja (gcc)"],
                                                 "Target architecture": ["64-bit", "32-bit"],
                                                 "Build mode": ["Release", "Debug"],
                                                 "Library type": ["Static", "Shared"],
                                                 "Build tests status": ["Yes", "No"]}

CfgFileValuesMapOfMap: dict[str, dict[str, str]] = {"Host platform": {"Linux": "Linux"},
                                                    "Toolchain": {"Ninja (gcc)": "Ninja (gcc)"},
                                                    "Target architecture": {"64-bit": "64-bit", "32-bit": "32-bit"},
                                                    "Build mode": {"Release": "Release", "Debug": "Debug"},
                                                    "Library type": {"Static": "Static", "Shared": "Shared"},
                                                    "Build tests status": {"Yes": "Yes", "No": "No"}}

def runCMakeConfigureCmd(cmd: str) -> None:
    run(cmd, shell=True)

def runCMakeBuildCmd(cmd: str) -> None:
    run(cmd, shell=True)

def buildCMakeCmds(cmake_file_folder_path: Path, build_folder_path: Path, cfg_details: dict[str, str]) -> tuple[str, str]:
    cmake_configure_cmd: str = f"cmake -S \"{cmake_file_folder_path}\" -B \"{build_folder_path}\""
    cmake_build_cmd: str = f"cmake --build \"{build_folder_path}\""

    if cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Ninja (gcc)"]:
        cmake_configure_cmd += " -G Ninja"
        cmake_configure_cmd += " -DCMAKE_CXX_COMPILER=g++"

    if cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Ninja (gcc)"]:
        if cfg_details["Target architecture"] == CfgFileValuesMapOfMap["Target architecture"]["64-bit"]:
            cmake_configure_cmd += " -DCMAKE_CXX_FLAGS=-m64"
        else:
            cmake_configure_cmd += " -DCMAKE_CXX_FLAGS=-m32"

    if cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Ninja (gcc)"]:
        if cfg_details["Build mode"] == CfgFileValuesMapOfMap["Build mode"]["Release"]:
            cmake_configure_cmd += " -DCMAKE_BUILD_TYPE=Release"
        else:
            cmake_configure_cmd += " -DCMAKE_BUILD_TYPE=Debug"

    if cfg_details["Library type"] == CfgFileValuesMapOfMap["Library type"]["Static"]:
        cmake_configure_cmd += " -DBUILD_STATIC_LIB__GW_LOG_SYS=TRUE"
    else:
        cmake_configure_cmd += " -DBUILD_STATIC_LIB__GW_LOG_SYS=FALSE"

    if cfg_details["Build tests status"] == CfgFileValuesMapOfMap["Build tests status"]["Yes"]:
        cmake_configure_cmd += " -DBUILD_TESTS__GW_LOG_SYS=TRUE"
    else:
        cmake_configure_cmd += " -DBUILD_TESTS__GW_LOG_SYS=FALSE"

    return (cmake_configure_cmd, cmake_build_cmd)

def rebuildFolder(folder_path: Path) -> None:
    if folder_path.exists():
        if folder_path.is_file():
            folder_path.unlink()  # delete file
        else:
            rmtree(folder_path, ignore_errors=True)

    folder_path.mkdir(parents=True, exist_ok=True)

def checkIfFolderExistsButItsIsEmpty(folder_path: Path) -> bool:
    if folder_path.exists() and not any(folder_path.iterdir()):
        return True
    else:
        return False

def makeSureFolderExists(folder_path: Path) -> bool:
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
        return True
    else:
        return False

def askUserIfTheyWantToForceReconfigureProject() -> bool:
    prompt: str = "Do you want to reconfigure the project?"
    options: list[str] = ["Yes", "No"]
    response: str = askUser(prompt, options)
    if response == "Yes":
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

def askUserIfTheyWantToLoadExistingCfgFile() -> bool:
    prompt: str = "Do you want to load existing cfg file?"
    options: list[str] = ["Yes", "No"]
    response: str = askUser(prompt, options)
    if response == "Yes":
        return True
    else:
        return False

def createNewCfgFile(file_path: Path, cfg_details: dict[str, str]) -> None:
    with open(file_path, "w") as file:
        for i in range(len(CfgFileHeadersList)):
            header: str = CfgFileHeadersList[i]
            value: str = cfg_details[header]

            file.write(f"[{header}]\n")

            if i < len(CfgFileHeadersList) - 1:
                file.write(f"{value}\n\n")
            else:
                file.write(f"{value}")

def askUserForCfgDetails() -> dict[str, str]:
    configuration: dict[str, str] = {
        "Host platform": "Linux",
        "Toolchain": "",
        "Target architecture": "",
        "Build mode": "",
        "Library type": "",
        "Build tests status": ""
    }

    prompt: str = "What toolchain to build with?"
    options: list[str] = CfgFileValuesMapOfLists["Toolchain"]
    response: str = askUser(prompt, options)
    configuration["Toolchain"] = response

    prompt: str = "What architecture does the target machine have?"
    options: list[str] = CfgFileValuesMapOfLists["Target architecture"]
    response: str = askUser(prompt, options)
    configuration["Target architecture"] = response

    prompt: str = "What build mode to build in?"
    options: list[str] = CfgFileValuesMapOfLists["Build mode"]
    response: str = askUser(prompt, options)
    configuration["Build mode"] = response

    prompt: str = "What type of library to build?"
    options: list[str] = CfgFileValuesMapOfLists["Library type"]
    response: str = askUser(prompt, options)
    configuration["Library type"] = response

    prompt: str = "Do you want to build tests?"
    options: list[str] = CfgFileValuesMapOfLists["Build tests status"]
    response: str = askUser(prompt, options)
    configuration["Build tests status"] = response

    return configuration

def askUser(prompt: str, options: list[str]) -> str:
    response: str = ""

    keep_asking: bool = True

    print(prompt)

    opt_index: int = 1
    for opt in options:
        print(f"{opt_index}. {opt}")
        opt_index += 1

    opt_chosen_index: int = 0
    while keep_asking:
        response = input()

        try:
            opt_chosen_index = int(response)
        except ValueError:
            print("[ERROR]: Input is not a number!")
            continue

        if opt_chosen_index < 1 or opt_chosen_index > len(options):
            print("[ERROR]: Input is out of range!")
            continue

        keep_asking = False

    return options[opt_chosen_index - 1]

def checkIfCfgFileExists(file_path: Path) -> bool:
    return file_path.exists()

def validateCfgFileContents(file_path: Path) -> None:
    segments_count_per_cfg_item: int = 3
    cfg_items_found_count: int = 0

    with open(file_path, "r") as file:
        line_index: int = 0
        cfg_item_index: int = 0
        current_header: str = ""

        for line in file:
            cfg_item_index = line_index % segments_count_per_cfg_item

            line = line.strip('\n')

            if cfg_item_index == 0:
                if not line.startswith('[') or not line.endswith(']'):
                    print("[ERROR]: Config item header doesn't start with a '[' or doesn't end with a ']'!")
                    print(f"[INFO]: Issue was found on line no. {line_index + 1}")
                    exit(1)

                line = line.lstrip('[')
                line = line.rstrip(']')

                if line not in CfgFileHeadersList:
                    print("[ERROR]: Config item header is invalid!")
                    print(f"[INFO]: Issue was found on line no. {line_index + 1}")
                    exit(1)

                current_header = line
            elif cfg_item_index == 1:
                if line not in CfgFileValuesMapOfLists[current_header]:
                    print("[ERROR]: Config item value is invalid!")
                    print(f"[INFO]: Issue was found on line no. {line_index + 1}")
                    exit(1)

                cfg_items_found_count += 1
            elif cfg_item_index == 2:
                if line != "":
                    print("[ERROR]: Config item empty line doesn't exist!")
                    print(f"[INFO]: Issue was found on line no. {line_index + 1}")
                    exit(1)

            line_index += 1

    if cfg_items_found_count != len(CfgFileHeadersList):
        print(f"[ERROR]: Found less or more config items then expected! Found {cfg_items_found_count} and expected {len(CfgFileHeadersList)}")
        exit(1)
                
if __name__ == "__main__":
    main()

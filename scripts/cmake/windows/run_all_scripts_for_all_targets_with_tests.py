from typing import Final
from pathlib import Path
from shutil import rmtree
from subprocess import run
from sys import executable

def main() -> None:
    cfg_details_list: Final[list[dict[str, str]]] = fillCfgDetailsList()

    project_root_folder_path: Final[Path] = Path(__file__).parents[3]
    build_folder_path: Final[Path] = project_root_folder_path / "build"

    total_count_of_configurations: int = len(cfg_details_list)
    current_configuration_index: int = 1

    current_script_folder_path: Final[Path] = Path(__file__).parent

    cfg_file_path: Final[Path] = Path(__file__).parents[1] / "cmake.conf"

    for configuration in cfg_details_list:
        print(f"[INFO]: Starting configuration no. {current_configuration_index} out of {total_count_of_configurations}.")

        createNewCfgFile(cfg_file_path, configuration)

        rebuildFolder(build_folder_path)

        cmake_file_folder_path: Path = project_root_folder_path
        cmake_configure_cmd: str = ""
        cmake_build_cmd: str = ""

        cmake_configure_cmd, cmake_build_cmd = buildCMakeCmds(cmake_file_folder_path, build_folder_path, configuration)

        runCMakeConfigureCmd(cmake_configure_cmd)

        runCMakeBuildCmd(cmake_build_cmd)

        run([executable, str(current_script_folder_path / "pack_single_target.py")])

        run([executable, str(current_script_folder_path / "run_tests_for_single_target.py")])

        print(f"[INFO]: Finished building and packing configuration no. {current_configuration_index} out of {total_count_of_configurations}.")
        current_configuration_index += 1

CfgFileHeadersList: list[str] =  ["Host platform", "Toolchain", "Target architecture", "Build mode", "Library type", "Build tests status"]

CfgFileValuesMapOfLists: dict[str, list[str]] = {"Host platform": ["Windows"],
                                                 "Toolchain": ["Ninja (clang)", "Visual Studio 17 2022 (msvc)"],
                                                 "Target architecture": ["64-bit", "32-bit"],
                                                 "Build mode": ["Release", "Debug"],
                                                 "Library type": ["Static", "Shared"],
                                                 "Build tests status": ["Yes", "No"]}

CfgFileValuesMapOfMap: dict[str, dict[str, str]] = {"Host platform": {"Windows": "Windows"},
                                                    "Toolchain": {"Ninja (clang)": "Ninja (clang)",
                                                                  "Visual Studio 17 2022 (msvc)": "Visual Studio 17 2022 (msvc)"},
                                                    "Target architecture": {"64-bit": "64-bit", "32-bit": "32-bit"},
                                                    "Build mode": {"Release": "Release", "Debug": "Debug"},
                                                    "Library type": {"Static": "Static", "Shared": "Shared"},
                                                    "Build tests status": {"Yes": "Yes", "No": "No"}}

def runCMakeBuildCmd(cmd: str) -> None:
    run(cmd)

def runCMakeConfigureCmd(cmd: str) -> None:
    run(cmd)

def buildCMakeCmds(cmake_file_folder_path: Path, build_folder_path: Path, cfg_details: dict[str, str]) -> tuple[str, str]:
    cmake_configure_cmd: str = f"cmake -S \"{cmake_file_folder_path}\" -B \"{build_folder_path}\""
    cmake_build_cmd: str = f"cmake --build \"{build_folder_path}\""

    if cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Ninja (clang)"]:
        cmake_configure_cmd += " -G Ninja"
        cmake_configure_cmd += " -DCMAKE_CXX_COMPILER=clang++"
    elif cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Visual Studio 17 2022 (msvc)"]:
        cmake_configure_cmd += " -G \"Visual Studio 17 2022\""

    if cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Ninja (clang)"]:
        if cfg_details["Target architecture"] == CfgFileValuesMapOfMap["Target architecture"]["64-bit"]:
            cmake_configure_cmd += " -DCMAKE_CXX_FLAGS=-m64"
        else:
            cmake_configure_cmd += " -DCMAKE_CXX_FLAGS=-m32"
    elif cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Visual Studio 17 2022 (msvc)"]:
        if cfg_details["Target architecture"] == CfgFileValuesMapOfMap["Target architecture"]["64-bit"]:
            cmake_configure_cmd += " -A x64"
        else:
            cmake_configure_cmd += " -A Win32"

    if cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Ninja (clang)"]:
        if cfg_details["Build mode"] == CfgFileValuesMapOfMap["Build mode"]["Release"]:
            cmake_configure_cmd += " -DCMAKE_BUILD_TYPE=Release"
        else:
            cmake_configure_cmd += " -DCMAKE_BUILD_TYPE=Debug"
    elif cfg_details["Toolchain"] == CfgFileValuesMapOfMap["Toolchain"]["Visual Studio 17 2022 (msvc)"]:
        if cfg_details["Build mode"] == CfgFileValuesMapOfMap["Build mode"]["Release"]:
            cmake_build_cmd += " --config Release"
        else:
            cmake_build_cmd += " --config Debug"

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
        rmtree(folder_path)

    folder_path.mkdir(exist_ok=True)

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

def fillCfgDetailsList() -> list[dict[str, str]]:
    configurations_list: list[dict[str, str]] = []
    current_configuration: dict[str, str] = {}

    for platform in CfgFileValuesMapOfLists["Host platform"]:
        for toolchain in CfgFileValuesMapOfLists["Toolchain"]:
            for arch in CfgFileValuesMapOfLists["Target architecture"]:
                for build_mode in CfgFileValuesMapOfLists["Build mode"]:
                    for library_type in CfgFileValuesMapOfLists["Library type"]:
                        current_configuration = {"Host platform": platform,
                                                 "Toolchain": toolchain,
                                                 "Target architecture": arch,
                                                 "Build mode": build_mode,
                                                 "Library type": library_type,
                                                 "Build tests status": CfgFileValuesMapOfMap["Build tests status"]["Yes"]}

                        configurations_list.append(current_configuration)

    return configurations_list

def checkIfCfgFileExists(file_path: Path) -> bool:
    return file_path.exists()

if __name__ == "__main__":
    main()

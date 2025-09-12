from pathlib import Path
from typing import Final
from shutil import rmtree
from shutil import copytree
from shutil import copy2
from os import mkdir
from subprocess import run
from os.path import isdir
from os import cpu_count
from time import time

def main() -> None:
    project_root_folder_path: Final[Path] = Path(__file__).parents[4]
    script_file_path: Final[Path] = Path(__file__)
    assest_folder_path: Final[Path] = script_file_path.parents[2] / "assets"
    temp_folder_path: Final[Path] = script_file_path.parents[2] / "temp"

    # Loading assest stage
    build_systems_supported_file_path: Final[Path] = assest_folder_path / "build_systems_supported.ini"
    generators_supported_file_path: Final[Path] = assest_folder_path / "generators_supported.ini"
    compilers_supported_file_path: Final[Path] = assest_folder_path / "compilers_supported.ini"
    architectures_supported_file_path: Final[Path] = assest_folder_path / "architectures_supported.ini"
    library_types_supported_file_path: Final[Path] = assest_folder_path / "library_types_supported.ini"

    build_systems_supported: Final[list[str]] = loadBuildSystemsSupportedFile(build_systems_supported_file_path)
    generators_supported: Final[dict[str, list[str]]] = loadGeneratorsSupportedFile(generators_supported_file_path)
    compilers_supported: Final[dict[str, list[str]]] = loadCompilersSupportedFile(compilers_supported_file_path)
    architectures_supported: Final[list[str]] = loadArchitecturesSupportedFile(architectures_supported_file_path)
    build_modes_supported: Final[list[str]] = ["Release"]
    library_types_supported: Final[list[str]] = loadLibraryTypesSupportedFile(library_types_supported_file_path)
    build_tests_status_supported: Final[list[str]] = ["No"]

    build_folder_path: Path = project_root_folder_path / "build"
    output_folder_path: Path = temp_folder_path / "output"
    project_name: str = "gw_log_sys"
    headers_folder_path: Path = project_root_folder_path / "library" / "include"
    tests_executable_file_name: str = "gw_log_sys_tests"

    start_build_total_time = time()
    buildProjectAndCopyImportantFiles(project_name, tests_executable_file_name, headers_folder_path,
                                      project_root_folder_path, build_folder_path, output_folder_path,
                                      build_systems_supported, generators_supported,
                                      compilers_supported, architectures_supported,
                                      build_modes_supported, library_types_supported,
                                      build_tests_status_supported)
    
    end_build_total_time = time()
    print(f"[INFO]: Finished building all targets! Elapsed time: {end_build_total_time - start_build_total_time:.2f} seconds.")

def buildProjectAndCopyImportantFiles(project_name: str, tests_executable_file_name: str, headers_folder_path: Path,
                                      project_root_folder_path: Path, build_folder_path: Path, output_folder_path: Path,
                                      build_systems_supported: list[str], generators_supported: dict[str, list[str]],
                                      compilers_supported: dict[str, list[str]], architectures_supported: list[str],
                                      build_modes_supported: list[str], library_types_supported: list[str],
                                      build_tests_status_supported: list[str]) -> None:
    build_system_folder_path: Path = Path()
    commands_list: dict[str, list[str]] = {}

    target_index: int = 1
    total_targets_count: int = 0

    target_folder_name: str = ""
    target_folder_path: Path = Path()
    important_item_paths: list[Path] = []

    total_targets_count += len(build_systems_supported)

    for build_system in build_systems_supported:
        # total number of compiler options for this build system
        compilers_count = sum(len(compilers_supported[gen]) for gen in generators_supported[build_system])
        total_targets_count *= compilers_count

    total_targets_count *= len(architectures_supported) * len(build_modes_supported) * len(library_types_supported) * len(build_tests_status_supported)

    for build_system in build_systems_supported:
        for generator in generators_supported[build_system]:
            for compiler in compilers_supported[generator]:
                for architecture in architectures_supported:
                    for build_mode in build_modes_supported:
                        for library_type in library_types_supported:
                            for build_tests_status in build_tests_status_supported:
                                rebuildBuildFolder(build_folder_path)

                                build_system_folder_path = getBuildSystemFolderPath(project_root_folder_path, build_system)

                                commands_list = constructCommands(build_system_folder_path,
                                                                  build_folder_path,
                                                                  build_system, generator,
                                                                  compiler, architecture,
                                                                  build_mode, library_type,
                                                                  build_tests_status)

                                print(f"[INFO]: Starting building process for target no. \"{target_index}\" out of \"{total_targets_count}\"...")
                                runCommands(build_system, commands_list)
                                print(f"[INFO]: Finished building process for target no. \"{target_index}\" out of \"{total_targets_count}\".")

                                target_folder_name = getTargetFolderName(build_system, architecture,
                                                                         generator, compiler,
                                                                         build_mode, library_type,
                                                                         build_tests_status)

                                target_folder_path = output_folder_path / target_folder_name

                                buildTargetFolder(target_folder_path)

                                important_item_paths = getImportantItemPathsList(build_folder_path, library_type,
                                                                                 build_tests_status, project_name,
                                                                                 tests_executable_file_name, headers_folder_path)

                                print(f"[INFO]: Starting: Copying important items for target no. \"{target_index}\" out of \"{total_targets_count}\"...")
                                copyImportantItemPathsToTargetFolder(important_item_paths, target_folder_path)
                                print(f"[INFO]: Finished copying important items for target no. \"{target_index}\" out of \"{total_targets_count}\".")

                                target_index += 1

def copyImportantItemPathsToTargetFolder(important_item_paths: list[Path], target_folder_path: Path) -> None:
    for item_path in important_item_paths:
        if isdir(item_path):
            parent_folder_path: Path = target_folder_path / item_path.name
            if not parent_folder_path.exists():
                mkdir(parent_folder_path)
            copytree(item_path, parent_folder_path, dirs_exist_ok=True)
        else:
            copy2(item_path, target_folder_path)

def getImportantItemPathsList(build_folder_path: Path, chosen_library_type: str,
                              chosen_build_tests_status: str, project_name: str,
                              tests_executable_file_name: str, headers_folder_path: Path) -> list[Path]:
    important_item_paths: list[Path] = []

    if chosen_library_type == "Static":
        important_item_paths.append(build_folder_path / f"lib{project_name}.a")
    elif chosen_library_type == "Shared":
        important_item_paths.append(build_folder_path / f"lib{project_name}.so")

    important_item_paths.append(headers_folder_path)

    if chosen_build_tests_status == "Yes":
        important_item_paths.append(build_folder_path / tests_executable_file_name)

    return important_item_paths

def buildTargetFolder(target_folder_path: Path) -> None:
    if not target_folder_path.exists():
        mkdir(target_folder_path)

def getTargetFolderName(chosen_build_system: str, chosen_architecture: str,
                        chosen_generator: str, chosen_compiler: str,
                        chosen_build_mode: str, chosen_library_type: str,
                        chosen_build_test_status: str) -> str:
    target_folder_name: str = "linux__"

    target_folder_name += f"{chosen_build_system.replace(' ', '_')}__"
    target_folder_name += f"{chosen_architecture.replace(' ', '_')}__"
    target_folder_name += f"{chosen_generator.replace(' ', '_')}__"
    target_folder_name += f"{chosen_compiler.replace(' ', '_')}__"
    target_folder_name += f"{chosen_build_mode.replace(' ', '_')}__"
    target_folder_name += f"{chosen_library_type.replace(' ', '_')}"

    if chosen_build_test_status == "Yes":
        target_folder_name += "__With_Tests"

    return target_folder_name

def runCommands(chosen_build_system: str, commands_list: dict[str, list[str]]) -> None:
    if chosen_build_system == "CMake":
        run(commands_list["Configuration"], check=True)
        run(commands_list["Building"], check=True)

def constructCommands(build_system_folder_path: Path,
                      build_folder_path: Path,
                      chosen_build_system: str, chosen_generator: str,
                      chosen_compiler: str, chosen_architecture: str,
                      chosen_build_mode: str, chosen_library_type: str,
                      chosen_build_tests_status: str) -> dict[str, list[str]]:
    commands_list: dict[str, list[str]] = {}
    current_command: list[str] = []
    current_command_segment: str = ""

    if chosen_build_system == "CMake":
        # Configuring stage
        current_command.append("cmake")
        current_command.append("-S")
        current_command.append(str(build_system_folder_path))
        current_command.append("-B")
        current_command.append(str(build_folder_path))

        if chosen_library_type == "Static":
            current_command.append("-DBUILD_STATIC_LIB__GW_LOG_SYS=TRUE")
        elif chosen_library_type == "Shared":
            current_command.append("-DBUILD_STATIC_LIB__GW_LOG_SYS=FALSE")

        if chosen_build_tests_status == "Yes":
            current_command.append("-DBUILD_TESTS__GW_LOG_SYS=TRUE")
        elif chosen_build_tests_status == "No":
            current_command.append("-DBUILD_TESTS__GW_LOG_SYS=FALSE")

        if chosen_build_mode == "Release":
            current_command.append("-DCMAKE_BUILD_TYPE=Release")
        elif chosen_build_mode == "Debug":
            current_command.append("-DCMAKE_BUILD_TYPE=Debug")

        if chosen_generator == "Ninja":
            current_command.append("-G")
            current_command.append("Ninja")

            current_command_segment = "-DCMAKE_CXX_FLAGS="

            if chosen_compiler == "Clang":
                current_command.append("-DCMAKE_CXX_COMPILER=clang++")

                current_command_segment += "-Wall -Wextra -Werror -Wconversion -pedantic"

                if chosen_architecture == "x86_64":
                    current_command_segment += " -target x86_64-pc-linux-gnu"
                elif chosen_architecture == "i686":
                    current_command_segment += " -target x86_64-pc-linux-gnu"

                if chosen_build_mode == "Release":
                    current_command_segment += " -O2 -DNDEBUG"
                elif chosen_build_mode == "Debug":
                    current_command_segment += " -O0 -g"
            elif chosen_compiler == "GCC":
                current_command.append("-DCMAKE_CXX_COMPILER=g++")
                current_command_segment += " -Wall -Wextra -Werror -Wconversion -pedantic"

                if chosen_architecture == "x86_64":
                    current_command_segment += " -m64"
                elif chosen_architecture == "i686":
                    current_command_segment += " -m32"

                if chosen_build_mode == "Release":
                    current_command_segment += " -O2 -DNDEBUG"
                elif chosen_build_mode == "Debug":
                    current_command_segment += " -O0 -g"

            current_command.append(current_command_segment)
        elif chosen_generator == "Make":
            current_command.append("-G")
            current_command.append("Unix Makefiles")

            current_command_segment = "-DCMAKE_CXX_FLAGS="

            if chosen_compiler == "Clang":
                current_command.append("-DCMAKE_CXX_COMPILER=clang++")
                current_command_segment += "-Wall -Wextra -Werror -Wconversion -pedantic"

                if chosen_architecture == "x86_64":
                    current_command_segment += " -target x86_64-pc-linux-gnu"
                elif chosen_architecture == "i686":
                    current_command_segment += " -target x86_64-pc-linux-gnu"

                if chosen_build_mode == "Release":
                    current_command_segment += " -O2 -DNDEBUG"
                elif chosen_build_mode == "Debug":
                    current_command_segment += " -O0 -g"
            elif chosen_compiler == "GCC":
                current_command.append("-DCMAKE_CXX_COMPILER=g++")
                current_command_segment += " -Wall -Wextra -Werror -Wconversion -pedantic"

                if chosen_architecture == "x86_64":
                    current_command_segment += " -m64"
                elif chosen_architecture == "i686":
                    current_command_segment += " -m32"

                if chosen_build_mode == "Release":
                    current_command_segment += " -O2 -DNDEBUG"
                elif chosen_build_mode == "Debug":
                    current_command_segment += " -O0 -g"

            current_command.append(current_command_segment)

        commands_list["Configuration"] = current_command
        
        # Building stage
        current_command = []
        current_command.append("cmake")
        current_command.append("--build")
        current_command.append(str(build_folder_path))

        num_cores = cpu_count()
        if not num_cores == None:
            max_threads = max(1, num_cores - 1)
            current_command.append("--")
            current_command.append(f"-j{max_threads}")

        commands_list["Building"] = current_command

    return commands_list
                                
def getBuildSystemFolderPath(project_root_folder_path: Path, chosen_build_system: str) -> Path:
    build_system_folder_path: Path = Path()

    if chosen_build_system == "CMake":
        build_system_folder_path = project_root_folder_path

    return build_system_folder_path

def rebuildBuildFolder(build_folder_path: Path):
    if build_folder_path.exists():
        rmtree(build_folder_path)
        mkdir(build_folder_path)
    else:
        mkdir(build_folder_path)

def loadLibraryTypesSupportedFile(file_path: Path) -> list[str]:
    library_types_found: list[str] = []

    with open(file_path, 'r') as file:
        for line in file:
            library_types_found.append(line.rstrip('\n'))

    return library_types_found

def loadBuildModesSupportedFile(file_path: Path) -> list[str]:
    build_modes_found: list[str] = []

    with open(file_path, 'r') as file:
        for line in file:
            build_modes_found.append(line.rstrip('\n'))

    return build_modes_found

def loadArchitecturesSupportedFile(file_path: Path) -> list[str]:
    architectures_found: list[str] = []

    with open(file_path, 'r') as file:
        for line in file:
            architectures_found.append(line.rstrip('\n'))

    return architectures_found

def loadCompilersSupportedFile(file_path: Path) -> dict[str, list[str]]:
    generators_found: dict[str, list[str]] = {}

    with open(file_path, 'r') as file:
        current_header: str = ""

        for line in file:
            line = line.rstrip('\n')
            if '[' in line:
                current_header = line.lstrip('[').rstrip(']')
                generators_found[current_header] = []
            elif len(line) != 0:
                generators_found[current_header].append(line)

    return generators_found

def loadGeneratorsSupportedFile(file_path: Path) -> dict[str, list[str]]:
    generators_found: dict[str, list[str]] = {}

    with open(file_path, 'r') as file:
        current_header: str = ""

        for line in file:
            line = line.rstrip('\n')
            if '[' in line:
                current_header = line.lstrip('[').rstrip(']')
                generators_found[current_header] = []
            elif len(line) != 0:
                generators_found[current_header].append(line)

    return generators_found

def loadBuildSystemsSupportedFile(file_path: Path) -> list[str]:
    build_systems_found: list[str] = []

    with open(file_path, 'r') as file:
        for line in file:
            build_systems_found.append(line.rstrip('\n'))

    return build_systems_found

if __name__ == "__main__":
    main()

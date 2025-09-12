from pathlib import Path
from typing import Final
from shutil import rmtree
from shutil import copy2
from shutil import copytree
from os import mkdir
from os import cpu_count
from os.path import isdir
from subprocess import run

def main() -> None:
    project_root_folder_path: Final[Path] = Path(__file__).parents[4]
    script_file_path: Final[Path] = Path(__file__)
    assest_folder_path: Final[Path] = script_file_path.parents[2] / "assets"
    temp_folder_path: Final[Path] = script_file_path.parents[2] / "temp"
    configurations_folder_path: Final[Path] = temp_folder_path / "configurations"

    # Loading assest stage
    build_systems_supported_file_path: Final[Path] = assest_folder_path / "build_systems_supported.ini"
    generators_supported_file_path: Final[Path] = assest_folder_path / "generators_supported.ini"
    compilers_supported_file_path: Final[Path] = assest_folder_path / "compilers_supported.ini"
    architectures_supported_file_path: Final[Path] = assest_folder_path / "architectures_supported.ini"
    build_modes_supported_file_path: Final[Path] = assest_folder_path / "build_modes_supported.ini"
    library_types_supported_file_path: Final[Path] = assest_folder_path / "library_types_supported.ini"

    build_systems_supported: Final[list[str]] = loadBuildSystemsSupportedFile(build_systems_supported_file_path)
    generators_supported: Final[dict[str, list[str]]] = loadGeneratorsSupportedFile(generators_supported_file_path)
    compilers_supported: Final[dict[str, list[str]]] = loadCompilersSupportedFile(compilers_supported_file_path)
    architectures_supported: Final[list[str]] = loadArchitecturesSupportedFile(architectures_supported_file_path)
    build_modes_supported: Final[list[str]] = loadBuildModesSupportedFile(build_modes_supported_file_path)
    library_types_supported: Final[list[str]] = loadLibraryTypesSupportedFile(library_types_supported_file_path)
    build_tests_status_supported: Final[list[str]] = ["Yes", "No"]

    # Prompting stage
    chosen_build_system: str = askUserWhichBuildSystem(build_systems_supported)

    cfg_file_path: Final[Path] = configurations_folder_path / f"{chosen_build_system}.ini"
    cfg_file_exists: Final[bool] = checkIfCfgFileExists(cfg_file_path)

    user_wants_to_reconfigure: bool = False

    if cfg_file_exists:
        user_wants_to_reconfigure = askUserIfTheyWantToReconfigure()

    make_fresh_configuration: Final[bool] = (not cfg_file_exists) or user_wants_to_reconfigure

    chosen_generator: str = ""
    chosen_compiler: str = ""
    chosen_architecture: str = ""
    chosen_build_mode: str = ""
    chosen_library_type: str = ""
    chosen_build_tests_status: str = ""

    build_folder_path: Path = project_root_folder_path / "build"

    if make_fresh_configuration:
        chosen_generator = askUserWhichGenerator(chosen_build_system, generators_supported)
        chosen_compiler = askUserWhichCompiler(chosen_generator, compilers_supported)
        chosen_architecture = askUserWhichArchitecture(architectures_supported)
        chosen_build_mode = askUserWhichBuildMode(build_modes_supported)
        chosen_library_type = askUserWhichLibraryType(library_types_supported)
        chosen_build_tests_status = askUserWhichBuildTestsStatus(build_tests_status_supported)

        saveToCfgFile(cfg_file_path,
                      chosen_generator, chosen_compiler,
                      chosen_architecture, chosen_build_mode, chosen_library_type,
                      chosen_build_tests_status)

        rebuildBuildFolder(build_folder_path)
    else:
        cfg_contents: dict[str, str] = loadFromCfgFile(cfg_file_path)

        chosen_generator = cfg_contents["Generator"]
        chosen_compiler = cfg_contents["Compiler"]
        chosen_architecture = cfg_contents["Target architecture"]
        chosen_build_mode = cfg_contents["Build mode"]
        chosen_library_type = cfg_contents["Library type"]
        chosen_build_tests_status = cfg_contents["Should build tests"]

    # Building the commands list stage
    build_system_folder_path: Path = getBuildSystemFolderPath(project_root_folder_path, chosen_build_system)

    commands_list: Final[dict[str, list[str]]] = constructCommands(build_system_folder_path,
                                                                   build_folder_path,
                                                                   chosen_build_system, chosen_generator,
                                                                   chosen_compiler, chosen_architecture,
                                                                   chosen_build_mode, chosen_library_type,
                                                                   chosen_build_tests_status)

    # Running commands list
    print("[INFO]: Starting building process...")
    runCommands(chosen_build_system, commands_list)
    print("[INFO]: Finished building process.")

    # Copy output files to output directory
    output_folder_path: Path = temp_folder_path / "output"

    target_folder_name: str = getTargetFolderName(chosen_build_system, chosen_architecture,
                                                  chosen_generator, chosen_compiler,
                                                  chosen_build_mode, chosen_library_type,
                                                  chosen_build_tests_status)

    target_folder_path: Path = output_folder_path / target_folder_name

    buildTargetFolder(target_folder_path)

    project_name: str = "gw_log_sys"

    headers_folder_path: Path = project_root_folder_path / "library" / "include"

    tests_executable_file_name: str = "gw_log_sys_tests"

    important_item_paths: list[Path] = getImportantItemPathsList(build_folder_path, chosen_library_type,
                                                                 chosen_build_tests_status, project_name,
                                                                 tests_executable_file_name, headers_folder_path)

    print("[INFO]: Starting: Copying important items...")
    copyImportantItemPathsToTargetFolder(important_item_paths, target_folder_path)
    print(f"[INFO]: Finished copying important items. They can be found at: {target_folder_path}")

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

def loadFromCfgFile(cfg_file_path: Path) -> dict[str, str]:
    found_header_value_pairs: dict[str, str] = {}

    with open(cfg_file_path, 'r') as file:
        for line in file:
            line = line.rstrip('\n')

            if '[' in line:
                line = line.lstrip('[').rstrip(']')
                found_header_value_pairs[line] = file.readline().rstrip('\n')
            else:
                continue

    return found_header_value_pairs

def saveToCfgFile(cfg_file_path: Path, chosen_generator: str,
                  chosen_compiler: str, chosen_architecture: str, chosen_build_mode: str,
                  chosen_library_type: str, chosen_build_tests_status: str) -> None:
    with open(cfg_file_path, 'w') as file:
        file.write(f"[Generator]\n")
        file.write(f"{chosen_generator}\n\n")

        file.write(f"[Compiler]\n")
        file.write(f"{chosen_compiler}\n\n")

        file.write(f"[Target architecture]\n")
        file.write(f"{chosen_architecture}\n\n")

        file.write(f"[Build mode]\n")
        file.write(f"{chosen_build_mode}\n\n")

        file.write(f"[Library type]\n")
        file.write(f"{chosen_library_type}\n\n")

        file.write(f"[Should build tests]\n")
        file.write(f"{chosen_build_tests_status}\n")

def checkIfBuildFolderExists(build_folder_path: Path) -> bool:
    return build_folder_path.exists()

def askUserIfTheyWantToReconfigure() -> bool:
    print("Do you want to reconfigure?")

    options: list[str] = ["Yes", "No"]

    option_index: int = 1
    for opt in options:
        print(f"{option_index}. {opt}")
        option_index += 1

    keep_asking: bool = True
    response_as_option_index: int = 0

    response: str = ""

    while(keep_asking):
        response = input()

        try:
            if (1 > int(response)) or (int(response) > len(options)):
                print("[ERROR]: Input out of range!")
                continue

            response_as_option_index = int(response) - 1
            keep_asking = False
        except ValueError:
            print("[ERROR]: Input is not a number!")

    if options[response_as_option_index] == "Yes":
        return True
    else:
        return False

def checkIfCfgFileExists(cfg_file_path: Path) -> bool:
    return cfg_file_path.exists()

def askUserWhichBuildTestsStatus(build_tests_status_supported: list[str]) -> str:
    print("Build tests?")

    option_index: int = 1
    for build_tests_status in build_tests_status_supported:
        print(f"{option_index}. {build_tests_status}")
        option_index += 1

    keep_asking: bool = True
    response_as_option_index: int = 0

    response: str = ""

    while(keep_asking):
        response = input()

        try:
            if (1 > int(response)) or (int(response) > len(build_tests_status_supported)):
                print("[ERROR]: Input out of range!")
                continue

            response_as_option_index = int(response) - 1
            keep_asking = False
        except ValueError:
            print("[ERROR]: Input is not a number!")

    return build_tests_status_supported[response_as_option_index]

def askUserWhichLibraryType(library_types_supported: list[str]) -> str:
    print("What library type?")

    option_index: int = 1
    for library_type in library_types_supported:
        print(f"{option_index}. {library_type}")
        option_index += 1

    keep_asking: bool = True
    response_as_option_index: int = 0

    response: str = ""

    while(keep_asking):
        response = input()

        try:
            if (1 > int(response)) or (int(response) > len(library_types_supported)):
                print("[ERROR]: Input out of range!")
                continue

            response_as_option_index = int(response) - 1
            keep_asking = False
        except ValueError:
            print("[ERROR]: Input is not a number!")

    return library_types_supported[response_as_option_index]

def askUserWhichBuildMode(build_modes_supported: list[str]) -> str:
    print("What build mode?")

    option_index: int = 1
    for build_mode in build_modes_supported:
        print(f"{option_index}. {build_mode}")
        option_index += 1

    keep_asking: bool = True
    response_as_option_index: int = 0

    response: str = ""

    while(keep_asking):
        response = input()

        try:
            if (1 > int(response)) or (int(response) > len(build_modes_supported)):
                print("[ERROR]: Input out of range!")
                continue

            response_as_option_index = int(response) - 1
            keep_asking = False
        except ValueError:
            print("[ERROR]: Input is not a number!")

    return build_modes_supported[response_as_option_index]

def askUserWhichArchitecture(architectures_supported: list[str]) -> str:
    print("What's the target architecture?")

    option_index: int = 1
    for architecture in architectures_supported:
        print(f"{option_index}. {architecture}")
        option_index += 1

    keep_asking: bool = True
    response_as_option_index: int = 0

    response: str = ""

    while(keep_asking):
        response = input()

        try:
            if (1 > int(response)) or (int(response) > len(architectures_supported)):
                print("[ERROR]: Input out of range!")
                continue

            response_as_option_index = int(response) - 1
            keep_asking = False
        except ValueError:
            print("[ERROR]: Input is not a number!")

    return architectures_supported[response_as_option_index]

def askUserWhichCompiler(chosen_generator: str, compilers_supported: dict[str, list[str]]) -> str:
    print("What compiler do you want to use?")

    option_index: int = 1
    for compiler in compilers_supported[chosen_generator]:
        print(f"{option_index}. {compiler}")
        option_index += 1

    keep_asking: bool = True
    response_as_option_index: int = 0

    response: str = ""

    while(keep_asking):
        response = input()

        try:
            if (1 > int(response)) or (int(response) > len(compilers_supported[chosen_generator])):
                print("[ERROR]: Input out of range!")
                continue

            response_as_option_index = int(response) - 1
            keep_asking = False
        except ValueError:
            print("[ERROR]: Input is not a number!")

    return compilers_supported[chosen_generator][response_as_option_index]

def askUserWhichGenerator(chosen_build_system: str, generators_supported: dict[str, list[str]]) -> str:
    print("What generator do you want to use?")

    option_index: int = 1
    for generator in generators_supported[chosen_build_system]:
        print(f"{option_index}. {generator}")
        option_index += 1

    keep_asking: bool = True
    response_as_option_index: int = 0

    response: str = ""

    while(keep_asking):
        response = input()

        try:
            if (1 > int(response)) or (int(response) > len(generators_supported[chosen_build_system])):
                print("[ERROR]: Input out of range!")
                continue

            response_as_option_index = int(response) - 1
            keep_asking = False
        except ValueError:
            print("[ERROR]: Input is not a number!")

    return generators_supported[chosen_build_system][response_as_option_index]

def askUserWhichBuildSystem(build_systems_supported: list[str]) -> str:
    print("What build system do you want to use?")

    option_index: int = 1
    for build_system in build_systems_supported:
        print(f"{option_index}. {build_system}")
        option_index += 1

    keep_asking: bool = True
    response_as_option_index: int = 0

    response: str = ""

    while(keep_asking):
        response = input()

        try:
            if (1 > int(response)) or (int(response) > len(build_systems_supported)):
                print("[ERROR]: Input out of range!")
                continue

            response_as_option_index = int(response) - 1
            keep_asking = False
        except ValueError:
            print("[ERROR]: Input is not a number!")

    return build_systems_supported[response_as_option_index]

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

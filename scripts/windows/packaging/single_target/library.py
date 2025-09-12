from typing import Final
from pathlib import Path
from subprocess import run

def main() -> None:
    script_file_path: Final[Path] = Path(__file__)
    assest_folder_path: Final[Path] = script_file_path.parents[2] / "assets"
    temp_folder_path: Final[Path] = script_file_path.parents[2] / "temp"
    configurations_folder_path: Final[Path] = temp_folder_path / "configurations"

    # Loading assest stage
    build_systems_supported_file_path: Final[Path] = assest_folder_path / "build_systems_supported.ini"
    build_systems_supported: Final[list[str]] = loadBuildSystemsSupportedFile(build_systems_supported_file_path)

    # Prompting stage
    chosen_build_system: str = askUserWhichBuildSystem(build_systems_supported)

    cfg_file_path: Final[Path] = configurations_folder_path / f"{chosen_build_system}.ini"
    cfg_file_exists: Final[bool] = checkIfCfgFileExists(cfg_file_path)

    if not cfg_file_exists:
        print("[ERROR]: Config file doesn't exist for the selected build system!")
        print("[INFO]: Run the build script again.")
        exit(1)


    cfg_contents: dict[str, str] = loadFromCfgFile(cfg_file_path)

    chosen_generator = cfg_contents["Generator"]
    chosen_compiler = cfg_contents["Compiler"]
    chosen_architecture = cfg_contents["Target architecture"]
    chosen_build_mode = cfg_contents["Build mode"]
    chosen_library_type = cfg_contents["Library type"]
    chosen_build_tests_status = cfg_contents["Should build tests"]

    target_folder_name: str = getTargetFolderName(chosen_build_system, chosen_architecture,
                                                  chosen_generator, chosen_compiler,
                                                  chosen_build_mode, chosen_library_type,
                                                  chosen_build_tests_status)

    output_folder_path: Path = temp_folder_path / "output"
    distribute_folder_path: Path = temp_folder_path / "distribute"

    target_folder_path: Path = output_folder_path / target_folder_name

    if not target_folder_path.exists():
        print("[ERROR]: Target folder doesn't exist!")
        print("[INFO]: Run the build script again.")
        exit(1)

    print("[INFO]: Starting: Archiving target folder build from previous configuration.")

    archive_file_path: Path = distribute_folder_path / f"{target_folder_name}.zip"

    archiveTargetFolder(archive_file_path, target_folder_path)

    print(f"[INFO]: Finished: Archiving target folder. Archive can be found at: {archive_file_path}")

def archiveTargetFolder(archive_file_path: Path, target_folder_path: Path) -> None:
    if archive_file_path.exists():
        archive_file_path.unlink()

    run(["powershell", "-Command", f"Compress-Archive -Path \"{target_folder_path}\" -DestinationPath \"{archive_file_path}\" -Force"], check=True)

def getTargetFolderName(chosen_build_system: str, chosen_architecture: str,
                        chosen_generator: str, chosen_compiler: str,
                        chosen_build_mode: str, chosen_library_type: str,
                        chosen_build_test_status: str) -> str:
    target_folder_name: str = "windows__"

    target_folder_name += f"{chosen_build_system.replace(' ', '_').replace('-', '_')}__"
    target_folder_name += f"{chosen_architecture.replace(' ', '_').replace('-', '_')}__"
    target_folder_name += f"{chosen_generator.replace(' ', '_').replace('-', '_')}__"
    target_folder_name += f"{chosen_compiler.replace(' ', '_').replace('-', '_')}__"
    target_folder_name += f"{chosen_build_mode.replace(' ', '_').replace('-', '_')}__"
    target_folder_name += f"{chosen_library_type.replace(' ', '_').replace('-', '_')}"

    if chosen_build_test_status == "Yes":
        target_folder_name += "__With_Tests"

    return target_folder_name

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

def checkIfCfgFileExists(cfg_file_path: Path) -> bool:
    return cfg_file_path.exists()

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

def loadBuildSystemsSupportedFile(file_path: Path) -> list[str]:
    build_systems_found: list[str] = []

    with open(file_path, 'r') as file:
        for line in file:
            build_systems_found.append(line.rstrip('\n'))

    return build_systems_found

if __name__ == "__main__":
    main()

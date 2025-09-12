from pathlib import Path
from typing import Final
from subprocess import run
from time import time

def main() -> None:
    script_file_path: Final[Path] = Path(__file__)
    temp_folder_path: Final[Path] = script_file_path.parents[2] / "temp"
    assest_folder_path: Final[Path] = script_file_path.parents[2] / "assets"

    output_folder_path: Path = temp_folder_path / "output"
    distribute_folder_path: Path = temp_folder_path / "distribute"

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
    library_types_supported: Final[list[str]] = loadLibraryTypesSupportedFile(library_types_supported_file_path)

    # Archiving target folders stage
    start_build_total_time = time()

    archiveAllTargetFolders(output_folder_path, distribute_folder_path,
                            build_systems_supported, generators_supported,
                            compilers_supported, architectures_supported,
                            library_types_supported)

    end_build_total_time = time()
    print(f"[INFO]: Finished archiving all targets! Elapsed time: {end_build_total_time - start_build_total_time:.2f} seconds.")

def archiveAllTargetFolders(output_folder_path: Path, distribute_folder_path: Path,
                           build_systems_supported: list[str], generators_supported: dict[str, list[str]],
                           compilers_supported: dict[str, list[str]], architectures_supported: list[str],
                           library_types_supported: list[str]) -> None:

    target_folder_name: str = ""
    archive_file_path: Path = Path()
    target_folder_path: Path = Path()

    target_index: int = 1
    total_targets_count: int = 0

    total_targets_count += len(build_systems_supported)

    for build_system in build_systems_supported:
        # total number of compiler options for this build system
        compilers_count = sum(len(compilers_supported[gen]) for gen in generators_supported[build_system])
        total_targets_count *= compilers_count

    total_targets_count *= len(architectures_supported) * len(library_types_supported)

    for build_system in build_systems_supported:
        for generator in generators_supported[build_system]:
            for compiler in compilers_supported[generator]:
                for architecture in architectures_supported:
                    for library_type in library_types_supported:
                        target_folder_name = getTargetFolderName(build_system, architecture,
                                                                 generator, compiler,
                                                                 library_type)

                        archive_file_path = distribute_folder_path / f"{target_folder_name}.zip"

                        target_folder_path = output_folder_path / target_folder_name

                        if archive_file_path.exists():
                            archive_file_path.unlink()

                        print(f"[INFO]: Starting: Archiving target folder no. \"{target_index}\" out of \"{total_targets_count}\"...")

                        run(["powershell", "-Command", f"Compress-Archive -Path \"{target_folder_path}\" -DestinationPath \"{archive_file_path}\" -Force"], check=True)

                        print(f"[INFO]: Finished: Archiving target folder no. \"{target_index}\" out of \"{total_targets_count}\".")

                        target_index += 1

def getTargetFolderName(chosen_build_system: str, chosen_architecture: str,
                        chosen_generator: str, chosen_compiler: str,
                        chosen_library_type: str) -> str:
    target_folder_name: str = "windows__"

    target_folder_name += f"{chosen_build_system.replace(' ', '_').replace('-', '_')}__"
    target_folder_name += f"{chosen_architecture.replace(' ', '_').replace('-', '_')}__"
    target_folder_name += f"{chosen_generator.replace(' ', '_').replace('-', '_')}__"
    target_folder_name += f"{chosen_compiler.replace(' ', '_').replace('-', '_')}__"
    target_folder_name += f"{chosen_library_type.replace(' ', '_').replace('-', '_')}"

    return target_folder_name

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

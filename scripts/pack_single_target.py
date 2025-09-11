from subprocess import run
from sys import executable
from typing import Final
from pathlib import Path

def main() -> None:
    requestPlatformFromUser()

def requestPlatformFromUser() -> None:
    prompt: str = "What platform are you on?"
    options: list[str] = ["Windows", "Linux"]
    platform_chosen: str = askUser(prompt, options)

    prompt: str = "What build system do you want to use?"
    options: list[str] = ["CMake"]
    build_system_chosen: str = askUser(prompt, options)

    current_script_folder_path: Final[Path] = Path(__file__).parent

    if platform_chosen == "Windows":
        if build_system_chosen == "CMake":
            run([executable, str(current_script_folder_path / "cmake" / "windows" / "pack_single_target.py")])
    elif platform_chosen == "Linux":
        if build_system_chosen == "CMake":
            run([executable, str(current_script_folder_path / "cmake" / "linux" / "pack_single_target.py")])

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

if __name__ == "__main__":
    main()

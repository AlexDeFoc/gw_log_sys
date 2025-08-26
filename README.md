# Logging system for gameWatch
A clean, portable, modern C++ 20 library

## Features
* Ability to log 'messages'
* Select which log level a message to be displayed as: none, info, warning, error, debug
* Limit the log level per 'logger', this way you can hide the debug log messages
* The log level tags are colored! (if your terminal can display the color)

## Download
Go to [Releases](https://github.com/AlexDeFoc/gw_log_sys/releases)
Choose & download the right file.

### Release file structure
|OS|Architecture|Compiler|Link type|
|--|------------|--------|---------|

## Building
### Requirements (one of each or all)
#### Scripts (optional)
* Powershell (Windows only)
* Manully run CMake
* Using some other extensions for CMake

#### Build system
* CMake - mandatory - version 4.1.0

#### Compilers
* Ninja
* Visual Studio 2022 / Build Tools for Visual Studio 2022
* GCC
* Clang

### Dependencies
* Testing framework - GoogleTest (Release tag: 1.17.0)

### CMake Options
* BUILD_TESTS - ON/OFF - ON by default - Builds executable containing tests
* BUILD_STATIC_LIBRARY - ON/OFF - OFF by default - Builds library to be linked statically

## Tested on
|Host OS   |Target OS |Host architecture|Target architecture|Compiler name|Compiler binary name     |Compiler source|Compiler version|
|----------|----------|-----------------|-------------------|-------------|-------------------------|---------------|----------------|
|Windows 11|Windows 11|64 bit           |64 bit             |Clang        |x86_64-pc-windows-msvc   |LLVM           |20.1.8          |
|Windows 11|Windows 11|64 bit           |32 bit             |Clang        |x86_64-pc-windows-msvc   |LLVM           |20.1.8          |
|Windows 11|Windows 11|64 bit           |64 bit             |GCC          |mingw-w64-ucrt-x86_64-gcc|MSYS           |14.2.0          |
|Windows 11|Windows 11|64 bit           |32 bit             |GCC          |mingw-w64-i686-gcc       |MSYS           |14.2.0          |
|Windows 11|Windows 11|64 bit           |64 bit             |MSVC         |                         |Visual Studio  |2022            |
|Windows 11|Windows 11|64 bit           |32 bit             |MSVC         |                         |Visual Studio  |2022            |

## Notes
### C++ Version
The project is set to compile using the C++ 23 version. It may be possible to compile using a older version of C++ but i don't guarrantee.

### Tested on list
The list refers to what platforms, using what compilers, ... , and it works on those computers.
It doesn't mean it can't work on other combinations or not listed in the list.
If it works on your machine, contribute!

### Library usability
This library is being actively used in the gameWatch app.
Beyond that, it can be used for other apps/uses, if needed to be modified it can be contributed to/forked/just used as is.

### Building requirements
The requirements are just the tools used to build all the releases.
You can choose one of each category: build system, compiler.

### Building tools versions
The versions listed are just the binaries versions used.
Building the project might work on older or newer versions.
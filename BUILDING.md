# Building guide

**Notes**:

* Every configuration presented here is just ones that have been tested to be working. Other ones may work too.
* Any version stated by '@' is the minimum version which was tested on, it may work with older or newer versions.
* Each configuration id corresponds to the actual output target folder and archive

## Chapters

* [Requirements](#requirements)
* [Steps](#steps)
* [Configurations](SUPPORTED.md#configurations)

# Requirements

**Note**: One of each

## Source control

* Git @ 2.47.3

## Build system

* CMake @ 4.1.1

## Scripting language

* Python @ 3.13.5

## Generator

* Ninja @ 1.12.1
* Make @ 4.4.1
* Visual Studio @ 17 2022

## Compiler

* Ninja
    * Clang @ 19.1.7
    * GCC @ 14.2.0

* Make
    * Clang @ 19.1.7
    * GCC @ 14.2.0

* Visual Studio
    * MSVC

## Architecture

* x86\_64 (64 bit)
* i686 (32 bit)

## Operating system

* Windows @ 11 24H2
* Linux @ Debian Trixie

# Steps

## Getting the project onto your machine

```
git clone https://github.com/AlexDeFoc/gw_log_sys.git
```

## Building a single target

```
cd gw_log_sys

cd scripts

cd (your platform)

cd building

cd single_target

python library.py
```

## Running a single target

**Note**: This will work only if you build the target with tests

```
cd gw_log_sys

cd scripts

cd (your platform)

cd running

python tests.py
```

## Packing a single target for distributing

```
cd gw_log_sys

cd scripts

cd (your platform)

cd packaging

cd single_target

python library.py
```

## Building all available targets

**Note**: This method only build targets without tests, and configure only for release

```
cd gw_log_sys

cd scripts

cd (your platform)

cd building

cd multi_target

python library.py
```

## Packaging all available targets

**Note**: This method only works after you've build all available targets previously

```
cd gw_log_sys

cd scripts

cd (your platform)

cd packaging

cd multi_target

python library.py
```

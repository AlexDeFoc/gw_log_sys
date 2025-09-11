# Building guide

**Note**: Every version is just one I've tested on, older version could work but it is recommened to use the latest versions or these at least

## Requirements

### Must have all

#### Source/version control tools

Git - 2.51.0

#### Building system generator

* CMake - version 4.1.1

#### Scripting tool

* Python - version 3.13.7

### Must have one of these from each category

#### Operating system

* Windows - version 24H2

#### Build system

* Ninja - version 1.13.1

#### C++ compiler able to compile C++23 source code

* Clang - version 21.1.0

## Building steps

**Note**: For building as a usual user follow the "Usual user/dev" category steps, else if you are a maintaner or are contributing follow the category called "Maintainer"

## Usual user/dev

### Cloning the repository to a folder called gw\_log\_sys

> git clone https://github.com/AlexDeFoc/gw\_log\_sys.git
 
### Going inside the folder which contains scripts to build the project

> cd scripts

### Running the build single target script

> python build\_single\_target.py

### Going inside the build folder and finding the build library and optionally if previously wished to build tests, the tests executable

> cd ..

> cd build

## Maintainer

### Cloning the repository to a folder called gw\_log\_sys

> git clone https://github.com/AlexDeFoc/gw\_log\_sys.git

### Going inside the folder which contains scripts to build the project

> cd scripts

### Running all scripts for a single target (build, test) - option 1

> python build\_single\_target.py

> python run\_tests\_for\_single\_target.py 

### Running all scripts for a single target (build, pack, test) - option 2

> python run\_all\_scripts\_for\_single\_target\_with\_tests.py

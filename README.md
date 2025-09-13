# gw\_log\_sys - Logging library

This is a C++ 23 library, that provides a way for the user to create message, set their logging level,
toggling their coloration individually. And a logger that prints the provided message to an
output stream (by default std::cout), setting its logging level limit,
if it should color any messages at all and more.

## Features

### Message object type

* Contains a text part, logging level part and should its logging level message part be colored
* It works with threads, async, futures and promises. Thus its thread safe.

### Logger object type

* Contains a logging level part and if it should color messages logging level message part
* It works with threads, async, futures and promises. Thus its thread safe.
* It can be used as a local variable or even as a singleton, by initializing it on the first "gather" of a handle to it.
Thus it can be used as a local variable or a singleton (working across cpp files), thread safe too.

### Other features

* Uses C++23
* Follows TDD & BDD
* Uses GoogleTest framework for testing
* Multi platform: Windows (11) & Linux (Debian Trixie)
* Thread safe
* Intuitive setters & getters, object methods, functions inside namespaces
* Its all organized in the gw::log namespace

## Documentation

Please go to the [wiki](https://github.com/AlexDeFoc/gw_log_sys/wiki) for documentation, how to use and the entire api (containing functions and other stuff). Also code examples!

## Building & Requirements for building

Please follow the guide and steps detailed in the file [BUILDING.md](https://github.com/AlexDeFoc/gw_log_sys/blob/main/BUILDING.md)

## Supported platforms & toolchains & On which were they tested on

Check out the file [SUPPORTED.md](https://github.com/AlexDeFoc/gw_log_sys/blob/main/SUPPORTED.md)

## Contributing in any way

Please follow the guide and steps detailed in the file [CONTRIBUTING.md](https://github.com/AlexDeFoc/gw_log_sys/blob/main/CONTRIBUTING.md)

## Reporting issues or suggesting features or reporting security issues

Please follow the guide and steps detailed in the file [CONTRIBUTING.md](https://github.com/AlexDeFoc/gw_log_sys/blob/main/CONTRIBUTING.md) and issues related more to security follow
the file [SECURITY.md](https://github.com/AlexDeFoc/gw_log_sys/blob/main/SECURITY.md)

## Code of conduct

Please follow the rules and guides detailed in the file [CODE\_OF\_CONDUCT.md](https://github.com/AlexDeFoc/gw_log_sys/blob/main/CODE_OF_CONDUCT.md)

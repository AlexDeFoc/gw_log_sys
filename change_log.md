# Change log
## Structure
|ID|Date       |Time |Authors  |
|--|-----------|-----|---------|
|10|2025-aug-24|10:20|Funny guy|

|Major|Minor|Patch|Release type     |
|-----|-----|-----|-----------------|
|1    |1    |2   |Release          |
|1    |2    |101  |Snapshot         |

|Changes               |Notes                                   |
|----------------------|----------------------------------------|
|Removed...            |It causing issues with...               |
|Added...              |Now we can use it for....               |
|Modified this... to...|No comment (change is self-explanatory).|

### Structure segments meaning
#### Major:
* May contain breaking changes

* Major changes relating syntax & performance

* May add new syntax or functionality

* May optimize a lot of stuff

* May bring major fixes that would lead to fatal crashes, errors, security
issues or wrong use

#### Minor:
* May modify stuff with the purpose of ease of use changes

* May bring slight optimization, general across many zones/files or to a
specific one

* May bring optizations for performance critical cases

* May bring small fixes that would sometimes crash the program, syntax issues or
general bugs

#### Patch:
* May bring general fixes to syntax issues, rare crashes, grammar issues,
forgotten to patch issues or issues introduced in the last release.

* May bring small optimizations that are beneficial to rare cases: high usage

#### Release type
##### Release
This release is 99% bug free, and destined to be the one uses for most cases.

##### Snapshot
This release is the latest version available (ussualy).

It doesn't guarrentee that bugs are all fixed, but they may...

This release has only been confirmed to be working on my machine.

It proposes new features that may not be introduced or may be removed before the
release candidate or release.

## Log entries
```
==========
8 | 2025-aug-26 | 16:27 | Sava Alexandru-Andrei
1.3.1
~~~~~~~~~~
* Changed all headers to use #pragma once
==========

==========
7 | 2025-aug-26 | 13:26 | Sava Alexandru-Andrei
1.3.0
~~~~~~~~~~
* Added ability to set text for a message using a std::string, not just const
char*
==========

==========
6 | 2025-aug-26 | 13:03 | Sava Alexandru-Andrei
1.2.0
~~~~~~~~~~
* Added the ability to initialize the logger with a log level

* Changed default log level for logger from k_info to k_none. This was changed
so that you have to either init with a certain log level or set it manually
using the SetLogLevel function.

* Changed in all headers the macro from _GW_LOG_SYSTEM... to _GW_LOG_SYS....
Actually forgot to do this, but now it's not necessary since change id #8
==========

==========
5 | 2025-aug-26 | 11:47 | Sava Alexandru-Andrei
1.1.1
~~~~~~~~~~
* Changed scripts to be able to compile with the new changes from gw_log_system
to gw_log_sys
==========

==========
4 | 2025-aug-26 | 11:37 | Sava Alexandru-Andrei
1.1.1
~~~~~~~~~~
* Adapted code by adding <format> in logger after the lowering of the C++
compilation version from C++23 to C++20
==========

==========
3 | 2025-aug-26 | 11:13 | Sava Alexandru-Andrei
1.1.0
~~~~~~~~~~
* Lowered C++ compilation version from C++23 to C++20
==========

==========
2 | 2025-aug-26 | 01:03 | Sava Alexandru-Andrei
1.1.0
~~~~~~~~~~
* CMakeLists.txt: changed tests to be build by default

* Separated LevelMessage from Level and moved the structure to a internal header

* Added color internal header

* Moved logic for choosing color for log level tag from ComposeMessage to
ColorizeLogLevelTag

* Added function that configures console on Windows to enable Virtual Text
Processing, thus being able to render colored text even on cmd

* Changed from inline to constexpr log level messages and colors
==========

==========
1 | 2025-aug-25 | 19:35 | Sava Alexandru-Andrei
1.0.0
~~~~~~~~~~
* Made the library | Finished it, but I plan to add really soon color to the log
level messages segment e.g. [INFO], [ERROR]...
==========
```
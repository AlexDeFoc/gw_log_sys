# Change log
## Structure
|ID|Date       |Time |Authors  |
|--|-----------|-----|---------|
|10|2025-aug-24|10:20|Funny guy|

|Major|Minor|Patch|Release type     |
|-----|-----|-----|-----------------|
|1    |0    |3    |Release candidate|
|1    |1    |13   |Release          |
|1    |2    |101  |Snapshot         |

|Changes               |Notes|
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
* May bring major fixes that would lead to fatal crashes, errors, security issues or wrong use

#### Minor:
* May modify stuff with the purpose of ease of use changes
* May bring slight optimization, general across many zones/files or to a specific one
* May bring optizations for performance critical cases
* May bring small fixes that would sometimes crash the program, syntax issues or general bugs

#### Patch:
* May bring general fixes to syntax issues, rare crashes, grammar issues, forgotten to patch issues or issues introduced in the last release.
* May bring small optimizations that are beneficial to rare cases: high usage

#### Release type
##### Release
This release is 99% bug free, and destined to be the one uses for most cases.

##### Release candidate
This release almost ready to be released but hasn't yet been verified on certain platforms, configurations or some bugs/issues haven't been yet fixed

##### Snapshot
This release is the latest version available (ussualy).
It doesn't guarrentee that bugs are all fixed, but they may...
This release has only been confirmed to be working on my machine.
It proposes new features that may not be introduced or may be removed before the release candidate or release.

## Log entries
```
==========
1 | 2025-aug-25 | 19:35 | Sava Alexandru-Andrei
~~~~~~~~~~
1.0.0R
~~~~~~~~~~
* Made the library | Finished it, but I plan to add really soon color to the log level messages segment e.g. [INFO], [ERROR]...
==========
```
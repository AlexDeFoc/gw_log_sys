> ### ID 2 - 2025 september 13 - 13:50 - 1.1.0
>
> ##### Sava Alexandru-Andrei `<alex.de.foc@gmail.com>`
>
> * Changed .clang-tidy so that it doesn't complain about using public normal variables inside structs
>
> * Modified structs & classes brackets style used in code to adhear to CONTRIBUTING.md
>
> * Modified CONTRIBUTING.md to apply the static variable prefix naming convention for more cases
>
> * Added new method "configure" for logger & message object types to be configured (all its or partial members) in one go, enabling
> users to not have to use mutex locks just to configure two or more members of a object type, and keep it threads safe.
>
> * Added more tests for the new configure method for both object types
>
> * Adding linux support, now users on linux can use ninja or make, clang or gcc
>
> * Reworked all scripts + building a target will attempt to use multiple threads (all possible - 1, to leave for no lag on the machine)
>
> * Fixed code for linux so it detects if the user terminal doesn't support color or the user has disabled it, it shall not
> display colored text, else display it

> ### ID 1 - 2025 september 10 - 23:50 - 1.0.0
>
> ##### Sava Alexandru-Andrei `<alex.de.foc@gmail.com>`
>
> * Configuring cmake and setup it
> * Making the python scripts for building, packing and testing the library & tests
> * Made the library & tests
> * Made & Added:
>
> CHANGELOG.md,
>
> LICENSE.md,
>
> CONTRIBUTING.md,
>
> CODE\_OF\_CONDUCT.md,
>
> SECURITY.md,
>
> SUPPORTED.md,
>
> README.md,
>
> BUILDING.md

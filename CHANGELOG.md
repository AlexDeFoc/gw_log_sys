> ### ID 2 - 2025 september 11 - 15:25 - 1.1.0
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
> * Fixed small writing issue in BUILDING.md, it was combining two lines into one visually
>
> * Changed inside scripts/cmake/windows/build\_single\_target.py so that it runs the cmd using shell=True (same on the linux side)
>
> * Adding linux support first with scripts + gcc + commands if needed + modifications to the code

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

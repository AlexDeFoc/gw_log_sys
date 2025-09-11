# Contributing guide

## Ways you can contribute

* Reporting issues, via the [issues tab](https://github.com/AlexDeFoc/gw_log_sys/issues)
* Suggesting new features, changes, via the [discussions tab](https://github.com/AlexDeFoc/gw_log_sys/discussions)
* Speaking with the community, via the [discussions tab](https://github.com/AlexDeFoc/gw_log_sys/discussions)
* Patching, modifying and improving the source code, after which proposing your work, via the [pull requests tab](https://github.com/AlexDeFoc/gw_log_sys/pulls)

## How to: report issues

Before reporting any issues please follow the issue template, via the [issues tab](https://github.com/AlexDeFoc/gw_log_sys/issues) when making a new issue.

That way the issue can be fixed much sooner.

Also be sure to choose the right template, based on your need. If you cannot find an appropriate template, you are allowed to create an issue without a template,
but only in the case you cannot choose a template.

## How to: suggest your ideas, changes, new features

The best way to suggest ideas is to talk about your ideas, via the [discussions tab](https://github.com/AlexDeFoc/gw_log_sys/discussions).

That way you won't hide more important issues, suggestions which are located in the issues tab.

After an idea or suggestion has been accepted, you may propose it as an issue in the [issues tab](https://github.com/AlexDeFoc/gw_log_sys/issues)
and attaching to it the "suggestion" **label**.

Once done, the devs will be going over the issue.

## How to: speak with the devs about *almost* anything

Via the [discussions tab](https://github.com/AlexDeFoc/gw_log_sys/discussions).

## How to: modify code and propose it

**IMPORTANT MESSAGE**

Before modifying any code, suggest your ideas, changes, via the [discussions tab](https://github.com/AlexDeFoc/gw_log_sys/discussions).

After your suggestion has been approved to be worth done, you may proceed to create an issue viat the [issues tab](https://github.com/AlexDeFoc/gw_log_sys/issues)
and attaching to it the "code suggestion" **label**

If you did partial code (not a lot), you have to still talk about it in the discussions tab, and keep the issue up, since its not final.

Once you've finished the code, you may propose it via the [pull requests tab](https://github.com/AlexDeFoc/gw_log_sys/pulls).

But before pushing a pull request, use a template, that way the devs can have an easier time reviewing the code.

After which the devs will be going over it. And trying to make it fit with the entire code, fixing stuff along the way and changing it if it doesn't
meet all the standards.

**Note**: If the proposed code doesn't follow most standards and imposes that the devs make more fixes then the proposed code, the code may be declined entirely.

### Making the code change

#### Standards needed to be met

* Building code by testing (similar to TDD & BDD)
* Trying to follow the naming conventions
* Trying to have a balance between convenience and performance
* Trying to not overcomplicate things just for the sake of convenience
* Trying to not make it hard for others to modify, build, test, or use the api

#### Notes

These are just suggestions. Meaning that you can go out of line but only if it makes sense for the api to be that way,
or for convenience for the user/dev.

If you don't know how to do something in a certain way, follow these guidelines, and only do different when you think it would make a
positive change.

#### How to code using testing

1. Make a test, give it a name of the behaviour you are targeting, or the general behaviour which will be observed
2. Write the api calls, variables all of it. Even though your lsp or other tools might scream at you because the stuff you write doesn't exist yet
3. Compile and run the tests executable, and read the error messages
4. Implement the code such that the test passes
5. If you did barely any just to pass the test, now its the time to make it better, finish the edges and make sure it performs well
6. If you wish to add more functionality, add that stuff to the existing test and repeat the previous steps, or make another test and repeat the previous tests

This way you know how the user or yourself will use, access the api

**Important note**: Try to do white box testing and not black box testing, that way you don't pollute the user api, and do poke holes if only
you expect other tools or features in the feature will use these, and the user using these is just for their own
testing or inspection of the object's containing data or functionality.

#### Returning type style for functions & methods

Always use trailing return type, never the old style

**Trailing return type**

Examples:

```
auto getMessage() const noexcept -> std::string_view;

auto setMessage(const std::string& new_msg_cpy) noexcept -> void;
```

#### Method modifiers

Use **noexcept**, **const** whenever possible and based on the use case. If a function needs to return something, for example using a getter function
return set the function modifier as **const** and return a constant reference to an object or a literal copy.

If you know the function cannot fail (throw an exception), (take into consideration the standard
c++ library which throws exceptions, handle them and fail according to the recommended way), set the method with the modifier **noexcept**.

#### Failing from a function

Instead of throwing exceptions, which is not allowed, and instead of returning an error value, or enum class member, we throw an "std::unexpected".

This implies we are using at the very least the C++23 standard.

#### Pointer and reference symbols placement

You shall place the pointer and reference symbols attached to the type and NOT to the variable name.

For example: `const char* variable_name` or `ObjectType& reference_to_an_object`

#### Initializing variables

You have to always initialize a variable with a value when *defined* (when it holds a place in memory).

It is not needed when declared (for example when using extern or function parameters)

If you are going to initialize a variable using a function make it on the same line
and if needed to be on the next line, initialize it using "{}" or with an invalid value

Examples:

```
std::string new_text{};
...using the actual new_text std::string

std::string another_text_string{"Hello World!"};

int i{0};

int a = getValue();
```

#### Initialization bracket style

Always you shall use the "{}" style for initialization.

It enforces not truncating values, imposes the dev to explicitly cast if needed to truncate data.

#### Type casting style

Always you shall use the `static_cast` style of cast instead of the C style cast.

And for the other use cases the correct one, `dynamic_cast` and the others if needed.

#### Naming case conventions

* Enum classes, structs, classes, enum members

**Pascal case**

Examples:

```
enum class UsingAsciColorsStatus { Enabled, NotPossible, Failed }

struct Item

class LoggingManager
```

* Methods (class/struct functions), free functions

**Camel case**

Examples:

```
void getLogLevelMessage()

auto setShouldColorChange()
```

* Variables, namespaces

**Snake case**

Examples:

```
static bool enabled_already

std::uint64_t title_lenght

namespace gw::log::testing_internals
```

#### Naming prefixes conventions

* Member variables (struct and class)

**"m\_"**

Examples:

```
static bool m_enabled_already

std::uint64_t m_title_lenght

const char* m_title
```

* Global variables

**"g\_"**

Examples:

```
static bool g_enabled_already

std::uint64_t g_title_lenght

const char* g_title
```

* Static variables (global, inside struct/class, inside functions)

**"s\_"**

Examples:

```
static bool s_enabled_already

static std::uint64_t s_title_lenght

const char* s_title
```

#### Bracket conventions by use case

* Struct, class, switch, case, function, method, scope withing function, if, else, while, for statements, sometimes lambda functions, sometimes enum classes (if too big)

**On new line**

Examples:

```
bool test()
{
}

if (int i = test())
{
}

for (auto i : v)
{
}

for (int i = 0; i < 1; ++i)
{
}

while (i != 1)
{
}
```

* Lambda functions, namespaces

**Opening on same line, ending on next line**

Examples:

```
namespace gw::log {
}

auto actionCheck = []() {
};
```

* Empty functions, empty methods, small enum classes

**Opening and closing on same line**

Examples:

```
gw::log::Logger::Logger() noexcept {}

void platformSpecificMethod() {}

enum class testingEnumClass : std::uint8_t { Enabled, Passed, Failed, NotPossible };
```

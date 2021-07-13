# C/C++ Code conventions

## Types
In C, always use defined type size instead of generic ones.
So use `uint16_t`, `int16_t`, `uint8_t`, etc instead of using `int`.


## Enums
* Whenever enums are used, the enum classes SHOULD be used.
* The naming of enum class MUST follow the UpperCamelCase naming convention, because it is a class.
* The values of the enums MUST follow the UPPER_CASE naming convention.

### Examples
#### Good example
``` cpp
enum class EnumExample
{
    FIRST_VALUE = 0,
    SECOND_VALUE = 1
};

EnumExample var = EnumExample::FIRST_VALUE; // call enum value via the scope of the enum class
```


## Null pointers
* When using C++11, `NULL` MUST NOT be used for null pointers. `nullptr` MUST be used instead.
* When using a compiler that does not support C++11, 0 MUST be used instead of `NULL`.


## Const vs Non-const
Whenever possible, `const` SHOULD be used. This is for both arguments declared in functions, the return values, and for the functions themselves (provided they don't change the internal state of the object).


## Implementation
The actual implementation SHOULD be in .cpp files. The only exceptions to this are template and inline functions, which MUST be implemented in the header file instead.


## Header guards
* Each header file MUST include a header guard.
* The actual header guard MUST use the UPPER_CASE naming convention.
* The closing `#endif` MUST be followed by a comment that states the header guard name used.


### Examples
#### Good Example
Example for a file in /src/folder/SomeClass.h
Note that the folder `src` is skipped, because all header and implementation files are in `src`.
``` cpp
#ifndef FOLDER_SOME_CLASS_H
#define FOLDER_SOME_CLASS_H

class SomeClass
{
};

#endif //FOLDER_SOME_CLASS_H
```


## Pointers and References
When declaring a variable, the asterisk `*` and the ampersand `&` should be connected to the type while leaving a space between it and the variable name.

### Examples
``` cpp
Object& instance; // Allowed
Object &instance; // Not allowed
```
Multiple declarations are allowed, as long as the objects have the same type
``` cpp
Object instance, other; // Allowed
Object* instance, other; // Not allowed, the other variable is of type Object, rather than Object*
```


## Forward declarations
Forward declarations SHOULD be used as often as possible to minimize the files included within headers.

### Examples
Example.h
``` cpp
#ifndef EXAMPLE_H
#define EXAMPLE_H
#include "Bar.h" // This needs an actual include, since we aren't just using a pointer.
class Foo; // The forward declaration.

class Example
{
public:
    Example();
    void doSomethingWithFooPointer(Foo* foo_pointer);
    void doSomethingWithBar(Bar bar);
}
```
Example.cpp
``` cpp
#include "Example.h"
#include "Foo.h" // Include is needed here, since the header only forwardly declared it.

Example::Example()
{
}

void Example::doSomethingWithBar(Bar bar)
{
}

void Example::doSomethingWithFooPointer(Foo* foo_pointer)
{
    foo_pointer->doSomething();
}
```

This document describes the code conventions and guidelines to be followed in Ultimaker C and C++ code.

Note that not all the code convention described here have been fully implemented yet. However, any newly committed code should follow the conventions below.


Code Conventions
=======
Below all code conventions which must be followed in all newly committed code.
The next section is on guidelines, which are allowed to be broken in certain cases.

Bracketing and indenting
-----
~~~~~~~~~~~~~~~{.cpp}
if (condition) // brackets always on new lines
{ // allways a bracket after an if, for, while, etc.
    // indent always with 4 spaces, never with tabs
}
else // else on new line
{
    // more code
}
~~~~~~~~~~~~~~~

Brackets may never be omitted. The opening and closing bracket should always be on a separate line on the same indentation level as the keywords (e.g. `if`, `while`, `else`). 
Any code within the brackets must be indented to one indentation level further. Indentation levels differ by 4 spaces.

Naming conventions
------
 * variables: lower_case_with_underscores
 * functions: lowerCamelCase
 * classes: UpperCamelCase
 * macros: UPPER_CASE_WITH_UNDERSCORES

Example:
~~~~~~~~~~~~~~~{.cpp}
#define UPPER_CASE_MACRO 1

class UpperCamelCaseClass
{
private:
    MemberVariableObject with_underscores;

public:
    void lowerCamelCaseFunction(ParamObject& also_with_underscores)
    {
        LocalObject under_scores;
    }
};
~~~~~~~~~~~~~~~

Enums
----
For C++, always use enum classes; never plain enums. Use UpperCamelCase for enum names and UPPER_CASE for the values.

Example:
~~~~~~~~~~~~~~~{.cpp}
enum class EnumExample 
{
    ELEM0 = 0,
    ELEM1 = 1
};

EnumExample var = EnumExample::ELEM0; // call enum value via the scope of the enum class
~~~~~~~~~~~~~~~

Spacing
----
Example:
~~~~~~~~~~~~~~~{.cpp}
for (int i = 0; i < len; i++)
{
    int j, k;
    j = k = 1 + mathematicalOperation(i);
    std::vector<int> l;
    vector.resize(len);
    vector[i] = j;
}
~~~~~~~~~~~~~~~
 * Binary operators (e.g. `+` `-` `*` `/` `=`) should always be enclosed by a space at both sides.
 * After a comma (`,`) there should be a space.
 * After keywords with brackets (e.g. `if`, `for`, `while`, `switch`) there should be a space.
 * In the `for` statement: place a space after the `;`, but not before.
 * When calling a function, place the opening bracket of the parameters right after the function name, without inserting a space.

Files
--------
Example for a file CuraEngine/src/foldr/SomeClass.h (UpperCamelCase):
~~~~~~~~~~~~~~~{.cpp}
#ifndef FOLDR_SOME_CLASS_H
#define FOLDR_SOME_CLASS_H

...

#endif//FOLDR_SOME_CLASS_H
~~~~~~~~~~~~~~~
Each header file must include a header guard as shown above. The defined macro is adopted from the path and name of the class and must follow the rules for macros (UPPER_CASE).
Here the folder `src` is skipped, because all header and implementation files of CuraEngine are in `src`.

Null pointer 
----
For C++, never use `NULL`, but use `nullptr` instead. NULL is an integer, not a pointer.

Ordering
----
 * There is yet no rule with respect to ordering private, protected and public class members.
 * There is yet no rule with respect to the ordering of arguments of functions. (Exception: optional arguments should always be at the end of the argument list.)





Illegal syntax
----
Here's some example of what is ***not*** allowed in any newly committed code:
~~~~~~~~~~~~~~~{.cpp}
void function()
{
    if (condition)
        single_line_outside_code_block(); // always use braces!
}; // unneccesary semicolon after function definition is not allowed
~~~~~~~~~~~~~~~

White Space
----
 * Don't leave trailing spaces at the end of a line.
 * Don't use tabs; use 4 spaces instead.


Code Guidelines
====
Below are a couple of guidelines which should generally be followed, unless there's good reason.

Implementation
----
Generally all implementation should be in .cpp files. An exception is template functions, which must be implemented in the header file.

Sometimes including the implementation in the header file can make it easier for the compiler to inline functions.

Class Files
----
It is generally preferred to have each class in its own file with a filename corrseponding to the class name.

Pointers vs. References
-----
(Under discusion)
Use reference wherever you can, pointers wherever you must.

Examples of where pointers can be used are:
- optional values
- variable values
- class members not known at construction

Documentation
----
We use [Doxygen](www.doxygen.org/) to generate documentation. Try to keep your documentation in doxygen style.

Doxygen documentation should always be next to the declaration of the thing documented - in the header file.

Here's a small example:
~~~~~~~~~~~~~~~{.cpp}
/*!
 * Doxygen style comments!
 *
 * \param param1 explanation may refer to another \p param2
 * \param param2 each parameter should be explained
 * \return explanation of what is returned
 */
int function(int param1, int param2)
{
    // non-doxygen style comments on implementation details
}

int member; //!< inline doxygen comment on the entry to the left
~~~~~~~~~~~~~~~

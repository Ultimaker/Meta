TODO
======
- QML
- JavaScript
- CSS

Code Conventions
=======
This document describes the code conventions and guidelines to be followed in all Ultimaker code, regardless the programming environment.

In certain cases specific rules might apply depening on the programming languaged used, but in general all the conventions would apply all programming and/or scripting languages.

Do note that not all the code convention described here have been fully implemented yet. However, any newly committed code should follow the conventions below.


Also check with PEP8 (https://www.python.org/dev/peps/pep-0008/) for Python and and Psr-2 (http://www.php-fig.org/psr/psr-2/) for PHP, C++ Best Practices on GitBook  (https://www.gitbook.com/book/lefticus/cpp-best-practices/details) for examples and ideas and so on and so forth.

These should be followed unless overruled in this document.

When contributing to other OpenSource projects, those coding guidelines must be followed.

Commenting
-----
There are 4 kinds of comments that can be used.
* Commenting foa doeumentation purposes (see Doxygen Commenting in different document)
* Comments to make clear something needs to be examined and possibly be refactored (referring to a Jira issue/story)
* Comments that are needed to explain a workaround to some unexpected behaviours
* In case of clariftying a choice made to implement something in a certain way, comments can be used to explain why

Comments in general never should state the obvious. If that's the case, rethink the strategy and solution.

###### JSON files
With Embedded, a adjustment is made to the parser of the JSON files to allow for comments.
This helps to describe what the parameters in the several JSON files mean and are used for.
Comments in the JSON file should start with a double /
Example:
~~~~~~~~~~~~~~~{.json}
// Temperature compensation used in marlin for control and reporting according to the following formula...
// compensated = (measured * factor) + offset
"temperature_compensation_hotends": {
    // No compensation
    "0": {
        "factor": 1.0,
        "offset": 0.0
    },
    // At measured 210.0 degrees C there is a discrepancy of -2.4 degrees C
    // Begin compensation starting at 50.0 degrees
    // Gain is 2.4 / (210.0 - 50.0)
    "1": {
        "factor": 0.985, // = 1.0 - gain
        "offset": 0.75   // = 50.0 * gain
    }
},
~~~~~~~~~~~~~~~

Logging
----
Logging should be done on a few levels: 
* DEBUG: Verbose logging -> logging data that is useful to debug parts of the code being run
* INFO: Logging -> logging information that can be seen as feedback to a user on his/her actions (acties gebruiker en acties systeem)
* WARN: Warning message are an indication to the user that something is not entirely right, but might not yet be a big issue
* ERROR: When a function cannot continue at all, but it doesnt mean that the application has to stop working.
* CRITICAL An error is a situation that cannot be overcome without external influence. This implies that the application is very likely to stop working at all

With the above guidelines, try to use common sense in what log level to use. Especially with DEBUG and INFO the border is not very clear.

*** New ***
uranium logging
python logging
[easylogging++ (boost)]
compile time log level?

Indenting / trailing whitespaces
-----
* Never use TABs
* Indenting is always 4 spaces
* No trailing whitespaces

Make sure that all editors used enforce these settings for the lines edited  changed (untouched code stays the same, unless a complete refactoring is going to happen)

Localization *** TODO ***
----
I8N strings?
embedded gelijk aan uranium
context marker + vertaling
use named arguments - this will help in the long run!
examples

Code blocks (not Code::Blocks :))
-----
* Always use a code block if possible and allowed in the language construction
* Code blocks always start on a new line
* The opening and closing code block delimiters should always be on a separate line on the same indentation level as the keywords (e.g. `if`, `while`, `else`).
* Any code within the a code block must be indented to one indentation level further. Indentation levels differ by 4 spaces.

Some examples of the previous rules:

Bad code
~~~~~~~~~~~~~~~{.cpp}
if (condition)       
{ cout << "Do nothing" << EOL; 
} else cout << "Hahaha" << EOL;
~~~~~~~~~~~~~~~
Good code
~~~~~~~~~~~~~~~{.cpp}
if (condition)
{ // New block, always start block delimiter on new line
    // indent always with 4 spaces, never with tabs
    cout << "Do nothing" << EOL;
} // Block end delimiter also on new line
else // else on new line
{ // A code block is always possible in this case, so use it
    cout << "Hahaha" << EOL;
}
~~~~~~~~~~~~~~~

Naming conventions
------
 * variables: lower_case_with_underscores
 * functions: lowerCamelCase
 * classes: UpperCamelCase
 * macros/constants: UPPER_CASE_WITH_UNDERSCORES

Function names should start with a verb (e.g. get, set, run, execute, validate etc.) or a question (e.g. is, has, can) as this helps a lot with understanding what the implementation is about.

QML exception -> own style

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

Enums (C/C++)
----
Always use enum classes; never plain enums. Use UpperCamelCase for enum names and UPPER_CASE for the values.

Example:
~~~~~~~~~~~~~~~{.cpp}
enum class EnumExample 
{
    ELEM0 = 0,
    ELEM1 = 1
};

EnumExample var = EnumExample::ELEM0; // call enum value via the scope of the enum class
~~~~~~~~~~~~~~~

Enum must follow the const rules.


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
 * Binary operators (e.g. `+` `-` `*` `/` `=` `+=` `-=` `/=` `*=`) should be enclosed by a space at both sides, except for the operators `->`, `.`, `->*`, `.*`, `,` and `::`.
 * After a comma (`,`) there should be a space - not before.
 * For keywords with parentheses `(` and `)` (e.g. `if`, `for`, `while`, `switch`) there should be a space in between the keyword and the opening parenthesis.
 * In the `for` statement: place a space after the `;`, but not before.
 * When calling a function, place the opening parenthesis `(` of the parameters right after the function name, without inserting a space.
 * When calling the index `[]` operator, don't insert a space before the `[`.


Static Typing (Python)
--------
Normally, Python is using dynamic typing. For example:
~~~~~~~~~~~~~~~{.py}
def fib(n):
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b

x = fib(5)
y = fib(2.5)
~~~~~~~~~~~~~~~
which defines the a dynamically typed function to return the Fibonacci number.
This will be fine for x, but what will the result be for y?

Adding more strict (static) typing can prevent these kinds of errors using tools like mypy (http://mypy-lang.org/):
~~~~~~~~~~~~~~~{.py}
from typing import Iterator

def fib(n: int) -> Iterator[int]:
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b

x = fib(5)
y = fib(2.5)
~~~~~~~~~~~~~~~
In this case, mypy will inform that the call using the floating point value is not valid:
__mypytest.py:10: error: Argument 1 to "fib" has incompatible type "float"; expected "int"__

This will help catching unwanted and unexpected bugs. This is not obligate but highly preferred and encouraged.

Header files (C/C++)
--------
Example for a file CuraEngine/src/folder/SomeClass.h (UpperCamelCase):
~~~~~~~~~~~~~~~{.cpp}
#ifndef (FOLDER_SOME_CLASS_H)
#define FOLDER_SOME_CLASS_H

...

#endif //FOLDER_SOME_CLASS_H
~~~~~~~~~~~~~~~
Each header file must include a header guard as shown above. The defined macro is adopted from the path and name of the class and must follow the rules for macros (UPPER_CASE).
Here the folder `src` is skipped, because all header and implementation files of CuraEngine are in `src`.

Pointers and References C(++)
----
When declaring a variable the asterisk (*) and the ampersand (&) should be connected to the type, and there should be a space between it and the variable name.
~~~~~~~~~~~~~~~{.cpp}
Object& instance; // allowed
Object &instance; // not allowed
~~~~~~~~~~~~~~~
Multiple declarations are allowed, as long as the objects have the same type
~~~~~~~~~~~~~~~{.cpp}
Object instance, other; // allowed
Object* instance, other; // not allowed, the other variable is of type Object, rather than Object*
~~~~~~~~~~~~~~~


Null pointer (C++)
----
For C++, never use `NULL`, but use `nullptr` instead. NULL is an integer, not a pointer.

Ordering
----
* Members: Implement functions Top-Down, starting with constructors/deconstructors in case of classes. That way, a class implementation can be read as a page from a book: from top to bottom providing clarity. This can be an issue for declarative language constructs like C/C++ , but then it's good practice to use forward declarations.
* Go from public, protected to private. Reasoning behind this is similar. When using a class, one is more interested in the public items. For inheriting the protected ones can be interesting, while the private parts should only be meaningfull to the maintainer of the class. This helps with the OOP paradigm of implementation hiding.

Strings
----
Strings are double quotes. While python and php allow single and double quoted strings, and PEP8 only says "pick a rule and stick to it". We decided to do double quotes to match C++.

Lines and Linelength
----
* "Maximum line length" - There is no hard limit on the line length, but as a thumb of rule, try to keep it to at most 120 characters. This helps doing the code reviews!
* A single line contains only one statement

Alignment
----
Align code for better readability.
This can be done on assignment level, parameter passing on function, array definitions and so on. 


Code Guidelines
====
Below are a couple of guidelines which should be followed, unless there's good reason not to.

Implementation (C/C++)
----
All implementations should be in .cpp files. An exception are template functions, which must be implemented in the header file.

Sometimes including the implementation in the header file can make it easier for the compiler to inline functions.

Class Files
----
Each class would have its own file with a filename corrseponding to the class name.
Hence a class named Printer would have a printer.h + printer.cpp for C/C++, a printer.py for Python and a printer.php for PHP

Namespaces
----
[ TO BE DISCUSSED ]

Const vs Non-const (C/C++)
----
The best practice is to use const when and wherever possible. This is for both arguments declared in functions as well as the return values of the functions and the functions themselves (when they don't change the internal state of the object).
In the long run this will make the code, libraries and runtime more stable and robust.
In the short run this might cause some friction with (older) code that does not use this concept (yet).

Pointers vs. References used as return values in argument list
-----
[ TO BE DISCUSSED ]
If arguments are allowed to be used to return values, then for all arguments everywhere, using doxygen commenting, [in] and [out] tags must be put in the comments describing the arguments.

Functions
----
* If a function needs to return more than one value, the return value could be a dictionary/hashtable construction or a specially defined struct, or via output parameters.
* The number of arguments to a function (especially when it's a member of a class) should not exceed 5. 
* [ Under discussion ] Functions should not contain more then 7-10 (?) lines of code. The pro is that functions have a more contained implementation leading to robust, testable, readable, less error-prone implementation. The con is that it will cause a bit more overhead (runtime calls) and documentation (for more functions)

Principles
----
Adhere to the following coding principles
* DRY instead of WET: Don't Repeat Yourself / (Write Everyting Twice, We Enjoy Typing)
* KISS: Keep It Simple, Stupid
* GRASP: General Responsibility Assignment Software Patterns
* SOLID: Single responsibility, Open-closed, Liskov substitution, Interface segregation and Dependency inversion (segregration of concern ^ 2)
*** TODO: explain above power acronyms ***

Documentation
====
[TODO]

We use [Doxygen](http://www.doxygen.org/) to generate documentation. Try to keep your documentation in doxygen style.

Doxygen documentation should always be next to the declaration of the thing documented - in the header file.

Here's a small example for C/C++
~~~~~~~~~~~~~~~{.cpp}
/*!
 * @brief Description about function
 * @param param1 explanation may refer to another \p param2
 * @param param2 each parameter should be explained
 * @return explanation of what is returned
 */
int function(int param1, int param2)
{
    // non-doxygen style comments on implementation details
}

int member; //!< inline doxygen comment on the entry to the left
~~~~~~~~~~~~~~~

Another example for Python
~~~~~~~~~~~~~~~{.py}
## Description about function
#  @param param1 explanation may refer to another \p param2
#  @param param2 each parameter should be explained, except for cls/self (comparable to this for C/C++)
#  @return explanation of what is being returned
def function(param1, param2):
    # Other comments
    ## description for variable
    some_var = 1

    return some_var * 10
~~~~~~~~~~~~~~~{.py}


These are still only basic options for doxygen.

Note: There is no colon between the argument name and the description. The first item which comes after @param should match the argument name.

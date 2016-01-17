Code Conventions
=======
This document describes the code conventions and guidelines to be followed in all Ultimaker code, regardless the programming environment.
In certain cases specific rules might apply depening on the programming languaged used, but in general all the conventions would apply all programming and/or scripting languages.

Do note that not all the code convention described here have been fully implemented yet. However, any newly committed code should follow the conventions below.

The Code Conventions are broken op in a few parts for better readability.

Commenting
-----
There are 3 kinds of comments that can be used.
* Commenting for documentation purposes (see Doxygen Commenting in different document)
* Comments to make clear something needs to be examined and possibly be refactored (referring to a Jira issue/story)
* Comments that are needed to explain a workaround to some unexpected behaviours

Never should comments be put in place to explain what code is (going to be) doing! 
If that's the case, rethink the strategy and solution.

Indenting / trailing whitespaces
-----
* Never use TABs
* Indenting is allways 4 spaces
* No trailing whitespaces

Make sure that all editors used enforce these settings

Code blocks
-----
* Allways use a codeblock if possible and allowed in the language construction
* Codeblocks allways start on a new line
* The opening and closing codeblock delimiters should always be on a separate line on the same indentation level as the keywords (e.g. `if`, `while`, `else`).
* Any code within the a codeblock must be indented to one indentation level further. Indentation levels differ by 4 spaces.

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
{ // New block, allways start block delimiter on new line
    // indent always with 4 spaces, never with tabs
    cout << "Do nothing" << EOL;
} // Block end delimiter also on new line
else // else on new line
{ // A code block is allways possible in this case, so use it
    cout << "Hahaha" << EOL;
}
~~~~~~~~~~~~~~~

Naming conventions
------
 * variables: lower_case_with_underscores
 * functions: lowerCamelCase
 * classes: UpperCamelCase
 * macros: UPPER_CASE_WITH_UNDERSCORES

Function names should start with a verb or a question (is, has) as this helps a lot with understanding what the implementation is about.

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


Header files (C/C++)
--------
Example for a file CuraEngine/src/foldr/SomeClass.h (UpperCamelCase):
~~~~~~~~~~~~~~~{.cpp}
#ifndef (PATH_SOME_CLASS_H)
#define PATH_SOME_CLASS_H

...

#endif //PATH_SOME_CLASS_H
~~~~~~~~~~~~~~~
Each header file must include a header guard as shown above. The defined macro is adopted from the path and name of the class and must follow the rules for macros (UPPER_CASE).
Here the folder `src` is skipped, because all header and implementation files of CuraEngine are in `src`.

Null pointer (C++)
----
For C++, never use `NULL`, but use `nullptr` instead. NULL is an integer, not a pointer.

Ordering
----
[MARCO: New advise]

* Members: Implement functions Top-Down, starting with constructors/deconstructors in case of classes. That way, a class implementation can be read as a page from a book: from top to bottom providing clarity. This can be an issue for declarative language constructs like C/C++ , but then it's good practice to use forward declarations.
* Go from public, protected to private. Reasoning behind this is similar. When using a class, one is more interested in the public items. For inheriting the protected ones can be interesting, while the private parts should only be meaningfull to the maintainer of the class. This helps with the OOP paradigm of implementation hiding.
* Optional arguments should always be at the end of the argument list.

Code Guidelines
====
Below are a couple of guidelines which should generally be followed, unless there's good reason not to.

Implementation
----
Generally all implementation should be in .cpp files. An exception is template functions, which must be implemented in the header file.

Sometimes including the implementation in the header file can make it easier for the compiler to inline functions.

Class Files
----
It is generally preferred to have each class in its own file with a filename corrseponding to the class name.

Pointers vs. References
-----
[Under discusion]
See also Const_Pointers_and_References.md

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

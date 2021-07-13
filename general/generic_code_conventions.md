# Code Conventions
This document describes the code conventions and guidelines to be followed in all Ultimaker code, regardless the programming environment / language.

In certain cases specific rules might apply, depending on the programming language used, but in general all the conventions apply to all programming and/or scripting languages.

Do note that not all the code convention described here have been fully implemented yet. However, any newly committed code MUST follow the conventions below, unless the document of the specific language overrides one or more of these rules.

When contributing to other (external / open source) projects, the coding guidelines of the respective projects MUST be followed.

## Commenting
There are 4 kinds of comments that can be used;
* Comments for interface / signature documentation purposes (see Doxygen Commenting in different document)
* Comments to indicate that something needs to be examined at a later stage and possibly be refactored. When this is done, it MUST be accompanied by a Jira issue / story. This means that every TODO comment must have a "connected" jira issue / story.
* Comments that explain a workaround. In these cases, the documentation must state why a work around is required instead of a "real" solution.
* Comments to clarify implementation decisions (eg; Why is something done in a certain way)

Comments in general never should state the obvious. If the comment is simply rephrasing the code, it should be left out.

### Examples
#### Bad Examples
``` python
# This is a function to do something.
# @param something an integer to which the function does doSomething
# @returns integer, the result of the something operation.
def doSomething(someting: int) -> int
  return something
```
``` python
foo = 20
foo += 20  # Add 20 to foo
```

## Logging
As a rule of thumb, logging is used to aid developers with debugging purposes, both while developing new features and fixing bugs "in the office", as well as resolving issues with software that is out in the field.

In order to provide some control and filtering to this logging, we've defined the following severity levels;
* **DEBUG**: The most verbose logging. This is intended for logging data that is useful to debug the code. It can be used to indicate state changes.
* **INFO**: Logging information that can be seen as feedback to a user on his/her actions, but without the information actually ending up with the user. For instance; Starting a print, print completed, etc.
* **WARNING**: Warning message are an indication that something that should have happened is not entirely the case. This is different from ERROR in such that it's not yet guaranteed to cause the code to cease working (for instance, because there is a fallback mechanism)
* **ERROR**: When piece of code cannot continue at all, but it doesn't  necessarily mean that the application has to stop working.
* **CRITICAL**: Critical indicates that there is a situation that cannot be overcome without external influence. This implies that the application is very likely to stop working at all.

Indenting / trailing whitespaces
-----
* You MUST NOT use TABs for indentation.
* Indenting MUST be done with 4 spaces per indentation level
* There MUST NOT be trailing whitespaces.

Make sure that all editors used enforce these settings, but only for the lines edited to ensure that untouched code remains the same.

Localization *** TODO ***
----
Although there is no full guideline for localization, the following things have been agreed on;
* Localization MUST be done by using .po files.
* You SHOULD use context hints

Code blocks (not Code::Blocks :))
-----
* Codeblocks should be used if possible and allowed in the language construction in case of `if`, `while`, `else` and `switch`.
* Codeblocks should also be used in the declarations of `classes` and `struct`'s.
* Opening braces should be on the same line as the keywords (e.g. `if`, `while`, `else`) with a single space between the keyword and the brace.
* Closing braces should be on the same indentation level as the keyword and on a new line after the code block.
* In the case of adding additional conditions such as using `else`, the second conditional check will be placed after the closing bracket of the first condition block, with a space in between.
* Any code within a code block must be indented one indentation level deeper.

The reasoning behind this setup is to save vertical space on the screen, whilst still upholding clear indentations and brackets that decrease the possibility of the existence of incomplete code blocks.

### Examples
#### Wrong code examples
``` cpp
if (condition)       
{ cout << "Do nothing" << EOL;
} else cout << "Hahaha" << EOL;
```
``` cpp
if (condition)
{ // New block, always start block delimiter on new line
    // indent always with 4 spaces, never with tabs
    cout << "Do nothing" << EOL;
} // Block end delimiter also on new line
else // else on new line
{ // A code block is always possible in this case, so use it
    cout << "Hahaha" << EOL;
}
```
#### Good code examples
``` cpp
if (condition) { // start block delimiter on the same line, add a single space
    cout << "Do nothing" << EOL; // indent always with 4 spaces, never with tabs
} else { // Closing brace should be on a new line, add spaces before and after the second conditional statement
    cout << "Hahaha" << EOL;
}

switch (variable) {
    case 1:
        do_this();
        break;
    case 2:
        do_that();
        break;
}
```


## Naming conventions
The following conventions are used for C/C++ naming. 
 * **variables**: `lower_case_with_underscores`
 * **functions**: `lowerCamelCase`
   > Note that we preceed the function name with a name scope or namespace. If required, that may be capitalized.
   This means that `planner_setMaxJerk()` is correct and `ADC128d818_readLimit()` is also correct.
 * **classes**: `UpperCamelCase`, or `PascalCase`
 * **macros/constants**: `UPPER_CASE_WITH_UNDERSCORES`

When possible, function names can start with a verb (e.g. get, set, run, execute, validate etc.) or a question (e.g. is, has, can) in order to help with understanding what the implementation is about.

> ! Note that at Ultimaker we follow the [Pep8](https://www.python.org/dev/peps/pep-0008/) coding standard. 
> This means we follow those naming conventions for Python.
> * **variables**: `lower_case_with_underscores`
> * **functions**: `lower_case_with_underscores` (different from our C/C++ standard)
> * **classes**: `CapWords`, which is the same as `PascalCase`
> * **macros/constants**: `UPPER_CASE_WITH_UNDERSCORES`

### Examples
#### Good code
``` cpp
#define UPPER_CASE_MACRO 1

class UpperCamelCaseClass
{
private:
    MemberVariableObject with_underscores;

public:
    void namespace_functionCapitalized(ParamObject& also_with_underscores)
    {
        LocalObject under_scores;
    }
};
```

### Solution for hotend versus nozzle and {}_index versus {}_nr or {}_number name usage:

 * MUST use 'hotend' for the hot part at the end of the extruder train, never 'nozzle'.
 * MUST only use 'nozzle' to refer to (attributes of) the Olsson block at the end of the hotend.
 * Renaming COULD be done according to the Boy-scout Rule. But SHOULD only in the same(/smallest) scope as where changes are made.
 * MUST only use '{}_index' indicating an index, counting value, referring to a position in an iterable. This will mostly be the case.
 * MUST only use '{}_number' indicating a counting value, referring to a ordinal number (e.g. first, second, third) nearly always used for communication to a user.

## Spacing
* Binary operators (e.g. `+` `-` `*` `/` `=` `+=` `-=` `/=` `*=`) MUST be enclosed by a space at both sides, except for the operators `->`, `.`, `->*`, `.*`, `,` and `::`.
* After a comma (`,`) there MUST be a space, but not before.
* In the `for` statement, a space MUST be after the `;`, but not before.
* When calling a function, the opening parenthesis `(` of the parameters MUST be placed directly after the function name, without inserting a space.
* When calling the index `[]` operator, don't insert a space before the `[`.
* If multiple parentheses groups tend to be unreadable, add spaces.
* Add 2 white lines between functions or 1 when the function has comments or documentation above its declaration.

### Examples
#### Good code
``` cpp
void examples_this_function(void) {
    for (int i = 0; i < len; i++)
    {
        int j, k;
        j = k = 1 + mathematicalOperation(i);
        std::vector<int> l;
        vector.resize(len);
        vector[i] = j;
        if ( (j == (k - 10)) && (k > 100) ) {   // you can add spaces between brackets to improve readability
            // do this
        }
    }
}

/**
 * @brief This function is commented, so a single white line is added in between
 */
void examples_that_function(void) {
    // some code
}
```

## Ordering
Functions SHOULD be implemented Top-Down, starting with constructors/deconstructors (in case of classes). That way, a class implementation can be read as a page from a book: from top to bottom. This can be an issue for declarative language constructs like C/C++ , but it's good practice to use forward declarations in the first place.

Go from public, protected to private. When using a class, one is usually more interested in the public items. For inheriting the protected ones can be interesting, while the private parts should only be meaningful to the maintainer of the class itself.

## Strings
Strings MUST be defined by using double quotes.

## Lines and length
There is no hard limit on the line length, but as a thumb of rule, try to keep it to at most 120 characters.
It is recommended to not let your IDE wrap lines. This allows for easier version control amongst peers. 

A single line SHOULD only contain one statement.

## Class Files
Each class SHOULD have its own file with a filename corresponding to the class name.

Hence a class named Printer would have a printer.h + printer.cpp for C/C++, a printer.py for Python and a printer.php for PHP.

Every class SHOULD be in it's own file, unless it's a private class.

## Namespaces
[ TO BE DISCUSSED ]

## Functions
* If a function needs to return more than one value, the return value could be a dictionary/hashtable construction or a specially defined struct.
* Output parameters SHOULD NOT be used in C++.
* The number of arguments to a function, especially when it's a member of a class, should not exceed 5.

## Documentation
[TODO]

We use [Doxygen](http://www.doxygen.org/) to generate documentation.

Doxygen documentation should always be above the declaration of the thing documented.
EpyText doxygen comments should used when working in Python.

If a source file needs explanation in it's usage, it should be added in the headers.

### Examples
#### Good examples
``` cpp
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
```

``` python
def function(param1: int, param2: int) -> int:
    """
    Description about function
    
    @param param1:  explanation may refer to another \p param2
    @param param2:  each parameter should be explained, except for cls/self (this is comparable to 'this' for C/C++)
    
    @rtype:         type of what is returned
    @return         explanation of what is being returned
    """
    some_var = 1

    return some_var * 10
```

>! Note: There is no colon between the argument name and the description. The first item which comes after @param should match the argument name.

Python Code Conventions
=======

General
---
Ultimaker adheres to the PEP8 coding guidelines as described here: https://www.python.org/dev/peps/pep-0008/,

** Important: **
Also check the code_conventions.md file for the generic rules, regardless of language.

With the following adjustments, exceptions and specific choices:
* See the 'line breaking' section below for specific suggested PEP8 style choices where function calls and definitions exceed the soft line length limit of 120 characters.
* MUST apply the following string formatting:
  * Multiple elements:
``` python
"{foo}_{bar}".format(foo = "foo", bar = "bar")
```
 * Single element:
``` python
"{}_bar".format("foo")
```
* SHOULD avoid circular dependencies as much as possible. Remove when encountered according to boy-scout rules.
* Parameters, variables and members MUST follow the lower_case_with_underscores convention.

Type checking
---
As per Ultimaker RFC-1,all new and changed code MUST be typed by using mypy typing. See: http://mypy-lang.org/ for more information.

## Bad example
Normally, Python is completely dynamically typed;
``` python
def fib(n):
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b

x = fib(5)
y = fib(2.5)
```
Which defines the a dynamically typed function to return the Fibonacci number.
This will be fine for x, but what will the result be for y?
## Good example
Adding more strict (static) typing can prevent these kinds of errors:
``` python
from typing import Iterator

def fib(n: int) -> Iterator[int]:
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b

x = fib(5)
y = fib(2.5)
```
In this case, mypy will inform that the call using the floating point value is not valid:
__mypytest.py:10: error: Argument 1 to "fib" has incompatible type "float"; expected "int"__

The following construct is _only_ allowed in case of unavoidable circular dependencies, otherwise regular import statements MUST be used.
``` python
MYPY = False
if MYPY:
    from [namespace] import [class]
```
Line breaking
---
Indentation of function definitions and function calls that exceed the soft line length (PEP8: 80, Ultimaker: 120 characters) is described in PEP8 https://www.python.org/dev/peps/pep-0008/#indentation. From the suggested set, the following SHOULD be applied:

When a function definition exceeds the maximum line length, wrap the lines as such:
``` python
def long_function_name(
    var_one: str,
    var_two: int,
    var_three: float,
    *,
    var_four: bool = False
) -> None:
    print(var_one)
```
for a function call:
``` python
foo = long_function_name(var_one, var_two,
    var_three, var_four = True
)
```
When encountering a long function call with named parameters, a newline MUST be used for each named parameter:
``` python
long_object_name.very_long_function_name(
    this_is_the_first_variable = var_one,
    this_is_the_second_variable = var_two
)
```
Most important guide to take into account here is the additional indent for each parameter. This MUST be used to separate the parameters from the logic in the function itself or following expressions in the case of a function call.

Quick references:
* Maximum line length: https://www.python.org/dev/peps/pep-0008/#maximum-line-length]
* Should a Line Break Before or After a Binary Operator: [https://www.python.org/dev/peps/pep-0008/#should-a-line-break-before-or-after-a-binary-operator]

Checker script(s)
=======
For everyones convenience, a pep8_check_python.py script is provided here. This script can check python code against this style guide. It depends on the pep8 package from: https://pypi.python.org/pypi/pep8

The usage of mypy (http://mypy-lang.org/) and pylint (https://www.pylint.org/) is strongly encouraged.

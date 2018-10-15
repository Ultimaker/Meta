Python Code Conventions
=======

General
---
Ultimaker adheres to the PEP8 coding guidelines as described here: https://www.python.org/dev/peps/pep-0008/,
with the following adjustments, exceptions and specific choices:

* Always use (4) spaces instead of tabs.
* Strings use double quotes to match C++ style.
* Maximum line length is set to 120 characters. See the 'line breaking' section below for specific suggested PEP8 style choices.
* String formatting, multiple elements:
``` python
"{foo}_{bar}".format(foo="foo", bar="bar")
```
* String formatting, single element:
``` python
"{}_bar".format("foo")
```
* Naming convention(s):
 * PEP8 specifies functions to be in lower_case_with_underscores. At Ultimaker we decided to match our C++ coding convention and use mixedCase (CapitalizedWords by initial lowercase character)
 * Parameters, variables and members follow the lower_case_with_underscores convention. PEP8 has no recommendation on this.
* Avoid circular dependencies as much as possible. Remove when encountered according to boy-scout rules.
* Check the code_conventions file for more (generic) rules.

Type checking
---
As per Ultimaker RFC-1, we require that all new and changed code is typed by using mypy typing. See: http://mypy-lang.org/ for more information.

## Bad example
Normally, Python is completely dynamicly typed;
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

The following construct is _only_ allowed in case of circular dependencies, otherwise use regular import statements.
``` python
MYPY = False
if MYPY:
    from [namespace] import [class]
```
Line breaking
---
Indentation of function definitions and function calls that exceed the maximum line length (PEP8: 80, Ultimaker: 120 characters) is described in PEP8 https://www.python.org/dev/peps/pep-0008/#indentation. From the suggested set, the following must be applied:

When a function definition exceeds the maximum line length, wrap the lines as such:
``` python
def long_function_name(
    var_one: str,
    var_two: int,
    var_three: float,
    *,
    var_four: bool=False
) -> None:
    print(var_one)
```
for a function call:
``` python
foo = long_function_name(var_one, var_two,
    var_three, var_four=True
)
```
When using long named parameters, use a newline for each named parameter:
``` python
long_object_name.very_long_function_name(
    this_is_the_first_variable=var_one,
    this_is_the_second_variable=var_two
)
```
Most important guide to take into account here is the additional indent for each parameter. This is used to separate the parameters from the logic in the function itself or following expressions in the case of a function call.

Quick references:
* Maximum line length: https://www.python.org/dev/peps/pep-0008/#maximum-line-length]
* Should a Line Break Before or After a Binary Operator: [https://www.python.org/dev/peps/pep-0008/#should-a-line-break-before-or-after-a-binary-operator]

Checker script(s)
=======
For everyones convenience, a pep8_check_python.py script is provided here. This script can check python code against this style guide. It depends on the pep8 package from: https://pypi.python.org/pypi/pep8

The usage of mypy (http://mypy-lang.org/) and pylint (https://www.pylint.org/) is strongly encouraged.

Python Code Conventions
=======

PEP8 is the code style guide for Python code used by the main python distribution.
This style guide can be found at:
https://www.python.org/dev/peps/pep-0008/

Our coding conventions follow the PEP style guide, with the exceptions stated in the generic code_conventions.md provided in this repository. This also means that for rules regarding class naming, documentation, etc., the rules described in the general code convention document MUST be used.

For convenience, these are re-listed here. In case of conflict, the generic code_conventions are considered to be leading.
* Always use spaces. While PEP8 allows tabs for backwards compatibility, we do not.
* Strings are double quotes. While Python allows single and double quoted strings, and PEP8 only says "pick a rule and stick to it". We decided to do double quotes to match C++.
* "Maximum line length" - PEP8 specifies a maximum line length of 79 characters. At Ultimaker we have no official line length limit, although we strive to keep lines below 120 characters.
* Naming convention:
  * Function names in PEP8 are in lower_case_with_underscores. At Ultimaker we decided to match our C++ coding convention and use mixedCase (CapitalizedWords by initial lowercase character).
  * Parameters, variables and members follow the lower_case_with_underscores convention. PEP8 has no recommendation on this.

As per Ultimaker RFC-1, we require that all new and changed code is typed by using mypy typing.

## Examples
### Bad example
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
### Good example
Adding more strict (static) typing can prevent these kinds of errors. At Ultimaker, we use mypy to perform this kind of checking. See: http://mypy-lang.org/ for more information.
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

Checker script(s)
=======
For everyones convenience, a pep8_check_python.py script is provided here. This script can check python code against this style guide. It depends on the pep8 package from: https://pypi.python.org/pypi/pep8

The usage of mypy (http://mypy-lang.org/) and pylint (https://www.pylint.org/) is strongly encouraged.

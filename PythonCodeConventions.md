Python Code Conventions
=======

PEP8 is the code style guide for Python code used by the main python distribution.
This style guide can be found at:
https://www.python.org/dev/peps/pep-0008/

Our coding conventions follow this style guide, with the following exceptions:
* Always spaces. While PEP8 allows tabs for backwards compatibility, we do not.
* Strings are double quotes. While python allows single and double quoted strings, and PEP8 only says "pick a rule and stick to it". We decided to do double quotes to match C++.
* "Maximum line length" - PEP8 specifies a maximum line length of 79 characters. At Ultimaker we have no official line length limit. And the general guideline is that the line should fit on your screen.
* Naming convention:
  ** PEP8 specifies functions to be in lower_case_with_underscores. At Ultimaker we decided to match our C++ coding convention and use mixedCase (CapitalizedWords by initial lowercase character)
  ** Parameters, variables and members follow the lower_case_with_underscores convention. PEP8 has no recommendation on this.

Checker script
=======
For everyone convenience, a pep8_check_python.py script is provided here. Which can check python code against this style guide. It depends on the pep8 package from: https://pypi.python.org/pypi/pep8 

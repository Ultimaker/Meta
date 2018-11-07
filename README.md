# Meta
This repository is used to document and define coding practices such as coding styles, writing commit messages and documentation.

The code_conventions.md defines the general coding conventions, without going into language specifics. It is possible that certain languages have their own coding standards. If this is the case, an additional document is added, which provides addendums or changes to the general codestyle.


## Structure

Each language specific file describes overrides to the Ultiamker Generic style rules, which themselves are an override of some comprehensive base set of rules. This means the override stucture is as follows:

```
             ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
   Top Layer │   UM Python   │ │    UM C++     │ │ UM JavaScript │ ...
             └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
                     ┆                 ┆                 ┆
                     ▼                 ▼                 ▼
             ┌────────────────────────────────────────────────────
Middle Layer │                     UM Generic                      ...
             └───────┬───────────────────────────────────┬────────
                     ┆                                   ┆
                     ▼                                   ▼
             ┌───────────────┐                   ┌───────────────┐
Bottom Layer │     PEP8      │                   │    AirBnB     │ ...
             └───────────────┘                   └───────────────┘
```

Within a language specific file, there should exist a "Structure" section which describes:

1. The bottom layer, e.g. "PEP8" or "AirBnB";
2. The middle layer, e.g. which parts of the bottom layer are overriden by UM Generic;
3. The top layer, e.g. which parts of UM Generic are overridden by that document;
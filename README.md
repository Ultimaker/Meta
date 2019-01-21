# Meta
This repository is used to document and define coding practices such as coding styles, writing commit messages and documentation.

## Structure
The files within the `/general` folder define general coding conventions while avoiding language specifics. It is possible that certain languages have their own coding standards. If this is the case, an additional document is added in the `/languages` folder which provides addendums or changes to the general codestyle. Useful files for development (such as standard linting or documentation configurations) can be found in the `/resources` folder.

## Language Files
Language files are expected to contain at least one of the following sections:

1. Code Style
2. Development Practices

### Code Style
Each language specific file describes overrides to the Ultiamker Generic style rules (`/general/generic_code_conventions.md`), which themselves are an override of some comprehensive base set of rules. This means the code style stucture is as follows:

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

### Development Practices
Unlike code style, development practices described in language-specific documents should not override company-wide development practices but can serve as an addendum where they contribute to the quality of the code written for a particular language.


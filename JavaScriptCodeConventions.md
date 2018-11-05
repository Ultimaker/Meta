# JavaScript Code Conventions
> NOTE: These conventions also apply to super-sets of JavaScript which are used within Ultimaker such as TypeScript.

## Introduction
These JavaScript style guidelines are intended to be used by both the R&D and marketing team as part of a broader effort to standardize JavaScript style across the company and as an early facilitator for the fact that Ultimaker continues to offer more web-based products such as the Cura Cloud services and Cura Connect.

## AirBnB as Baseline Style
To reduce the need to build comprehensive style guidelines ourselves, we have decided to adopt the well-known and widely used **AirBnB style**. The full documentation for AirBnB style [can be found on GitHub](https://github.com/airbnb/javascript). For the most part, this style is already very similar to what is used by front-end teams at Ultimaker with a few differences, which are outlined below. It was also chosen because of it was designed for usage with React.js, which is used by the R&D department. It is applicable to Vue.js as well, however, and can be used by the marketing department.

## Enforcing AirBnB Style in Your Editor
### Set-Up for VS Code
1. Install packages:

```
npm i --save-dev eslint eslint-config-airbnb eslint-plugin-import eslint-plugin-jsx-a11y eslint-plugin-react typescript-eslint-parser
```
2. Install the [`eslint` plugin for VS Code](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint).
3. Create an `.eslintrc.json` file in your project’s root directory.
4. Add the following content to `.eslintrc.json`:

```
{
    "extends": "airbnb",
    "env": {
        "node": true,
        "es6": true,
        "browser": true
    },
    "parserOptions": {
        "ecmaVersion": 6,
        "sourceType": "module",
        "ecmaFeatures": {
            "modules": true,
            "jsx": true
        }
    },
    "plugins": ["import"],
    "rules": {
        "indent": ["error", 4, {
            "ignoredNodes": ["JSXElement", "JSXElement > *", "JSXAttribute", "JSXIdentifier", "JSXNamespacedName", "JSXMemberExpression", "JSXSpreadAttribute", "JSXExpressionContainer", "JSXOpeningElement", "JSXClosingElement", "JSXText", "JSXEmptyExpression", "JSXSpreadChild"]
        }],
        "no-underscore-dangle": 0,
        "import/no-unresolved": 0
    },
    "settings": {
        "import/extensions": [".js", ".jsx"]
    },
    "overrides": [
        {
            "files": ["**/*.ts", "**/*.tsx"],
            "parser": "typescript-eslint-parser",
            "rules": {
                "no-undef": 0,
                "react/jsx-filename-extension": [1, {
                    "extensions": [".tsx"]
                }],
                "jsx-closing-tag-location": 0
            },
            "settings": {
                "import/extensions": [".ts", ".tsx"]
            }
        }
    ]
}
```

## Additions to AirBnB
### Comments
Use JSDoc style comments.

### Typing
TypeScript types/interfaces should use PascalCase.

## Exceptions to AirBnB
### Tabs
Although AirBnB prescribes 2 spaces for indentation, _all_ of Ultimaker software (R&D and Marketing) already use 4 spaces as a standard. For this reason an exception is added in `.eslintrc.json`.

### Underscores
One difficult change which will need to be adapted over time is the elimination of underscores. For this rule, an exception can be made until projects are converted to TypeScript, at which point the AirBnB style will be followed with an additional caveat.

- **Existing:** Private properties/methods should start with an underscore (\_).
- **AirBnB:** JavaScript does not have a concept of private, so do not make “fake private” properties/methods with an underscore.
- **Future:** TypeScript _does_ have a concept of private, so the TypeScript prefix `private` should be used to denote private properties/methods instead of an underscore.


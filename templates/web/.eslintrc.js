module.exports = {
    extends: "airbnb",
    env: {
        node: true,
        es6: true,
        browser: true
    },
    parserOptions: {
        ecmaVersion: 6,
        sourceType: "module",
        ecmaFeatures: {
            modules: true,
            jsx: true
        }
    },
    plugins: ["import"],
    rules: {
        "indent": ["error", 4, {
            "ignoredNodes": [
                "JSXElement",
                "JSXElement > *",
                "JSXAttribute",
                "JSXIdentifier",
                "JSXNamespacedName",
                "JSXMemberExpression",
                "JSXSpreadAttribute",
                "JSXExpressionContainer",
                "JSXOpeningElement",
                "JSXClosingElement",
                "JSXText",
                "JSXEmptyExpression",
                "JSXSpreadChild"
            ]
        }],
        "no-underscore-dangle": 0,
        "import/no-unresolved": 0
    },
    settings: {
        "import/extensions": [".js", ".jsx"]
    },
    overrides: [
        {
            files: ["**/*.ts", "**/*.tsx"],
            parser: "typescript-eslint-parser",
            rules: {
                "no-undef": 0,
                "react/jsx-filename-extension": [1, {
                    "extensions": [".tsx"]
                }],
                "jsx-closing-tag-location": 0
            },
            settings: {
                "import/extensions": [".ts", ".tsx"]
            }
        }
    ]
}
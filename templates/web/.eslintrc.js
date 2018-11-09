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

            // These overrides are required to keep React code looking good
            // They don't affect non-React code
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
        "import/no-unresolved": 0,
        "jsx-closing-tag-location": 0
    },
    settings: {
        "import/extensions": [".js", ".jsx"]
    },

    // Create some special overrides for TypeScript files
    overrides: [
        {
            files: ["**/*.ts", "**/*.tsx"],
            parser: "typescript-eslint-parser",
            rules: {

                // Required for interfaces
                "no-undef": 0,

                // Use .tsx instead of .jsx
                "react/jsx-filename-extension": [1, {
                    "extensions": [".tsx"]
                }]
            },
            settings: {

                // Allow import of .ts and .tsx without specifying extension
                "import/extensions": [".ts", ".tsx"]
            }
        }
    ]
}
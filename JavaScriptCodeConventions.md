# JavaScript Code Conventions
> NOTE: These conventions also apply to super-sets of JavaScript which are used within Ultimaker such as TypeScript. As of November 2018, this document does not apply to QML/JS within QML.

## Contents
1. [Introduction](#introduction)
2. [Structure](#structure)
3. [Applying these Conventions in your Editor](#applying-these-conventions-in-your-editor)

## Introduction
These JavaScript style guidelines are intended to be used by both the R&D and marketing team as part of a broader effort to standardize JavaScript style across the company and as an early facilitator for the fact that Ultimaker continues to offer more web-based products such as the Cura Cloud services and Cura Connect.

## Structure
Per the convention for `Ultimaker/Meta`, rules within this document override Ultimaker Generic rules (`code_conventions.md`), which override the baseline standard (AirBnB). These can be considered a bottom, middle, and top layer of the standard.

### Bottom Layer: AirBnB
As a foundation, Ultimaker uses the well-known and widely used **AirBnB style**. The full documentation for AirBnB style [can be found on GitHub](https://github.com/airbnb/javascript).

> **Why?** For the most part, this style is already very similar to what is used by front-end teams at Ultimaker. It was also chosen because of it was designed for usage with React.js, which is used by the R&D department.

### Middle Layer: UM Generic
In certain places, the UM Generic style (`code_conventions.md`) overrides AirBnB style. These exceptions can be inferred by comparing the two documents, however for clarity they are as follows:

- Use 4 spaces for indentation.

	```ts
	// Bad
	class Foo {
	  bar: true;
	}

	// Good
	class Foo {
	    bar: true;
	}
	```
	
- Use 1-2 leading underscores to denote protected and private properties (respectively).

	```ts
	class Foo {

	    // Properties
	    publicThing: 8;
	    _protectedThing: "bar";

	    // Methods
	    refresh() {
	        // Do some things...
	        this._updateInterally();
	    }
	    _updateInterally() {
	        // Do the update...
	    }
	}
	```

### Top Layer: UM JavaScript
In certain cases, the UM JavaScript style overrides the UM Generic style (`code_conventions.md`). These exceptions can be inferred by comparing the two documents however for clarity they are as follows:

- Use camelCase for both variable names and method/function names.

	> **Why?** In JavaScript, functions are variables, and camelCase is effectively industry-standard.
	
	```js
	class Fooinator {

	    constructor() {
	        this._fooBar = 0;
	    }

	    get fooBar() {
	        return this._fooBar;
	    }

	    makeMoreFoo() {
	        this._fooBar++;
	    }
	}
	```

- Always put brackets on the same line .

	> **Why?** Readability is improved and same-line is effectively industry-standard.
	
	```js
	// Bad
	class Foo
	{
	    constructor()
	    {
	        if (this.bar)
	        {
	            // Do something...
	        }
	    }
	}

	// Good
	class Foo {
	    constructor() {
	        if (this.bar) {
	            // Do something...
	        }
	    }
	}
	```
	
- Use single quotes instead of double quotes.

	> **Why?** In web contexts, when writing JS and HTML in the same file, it’s typical to use double quotes for HTML and single quotes for JS.
	
	```js
	// Bad
	const foo = "bar";

	// Good
	const foo = 'bar';
	```
	
Some additional rules which are not addressed on lower levels are as follows:

- Documentation must use JSDoc style comments.

	```js
	/**
	 * Creates a book.
	 * @param {string} title - The title of the book.
	 * @param {string} author - The author of the book.
	 */
	function makeBook(title, author) {
	    // Make the book...
	}
	```

- TypeScript types/interfaces should use PascalCase.

	```ts
	interface FooComponentProps {
		foo: number;
		bar: boolean;
	}

	class FooComponent extends React.Component<FooComponentProps> {
		// Make the component...
	}
	```

## Applying these Conventions in your Editor
### Set-Up for VS Code
1. Install packages:

```
npm i --save-dev eslint eslint-config-airbnb eslint-plugin-import eslint-plugin-jsx-a11y eslint-plugin-react typescript-eslint-parser
```
2. Install the [`eslint` plugin for VS Code](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint).
3. Copy the files from `templates/web` within this repostory to the root directory of your project.
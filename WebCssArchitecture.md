CSS Architecture
================

Architectural principles
------------------------

- The UI-design principles(language) and CSS naming share a common structure
- Mobile first, so the device with smallest screen has less css parsing
- [Single responsibility principle](https://en.wikipedia.org/wiki/Single_responsibility_principle)
- Components have there own namespace so they can be refactored
- Use predictable CSS rules
- CSS must be self documenting
- Preferably keep the [specificity](https://css-tricks.com/specifics-on-css-specificity/ at one class selectors or
 element selector (0,0,1,0 or 0,0,0,1)
- Max depth of applicability: 1

Tools and methodologies
-----------------------

### Translating to a CSS Structure
The main goal of a good CSS structure is to support with css specifics like namespacing, cascading and
 specificity. In order to not end up in a specificity war we need to split up the css order in layers and set the
 layer order from global to specific to finally end with global states (like this .is-hidden class).

The Inverted Triangle CSS structure is the current de facto standard to structure css:

- **Settings**: Font, colors definitions, etc.
- **Tools**: Globally used mixins and functions. The atomic design library is imported (referenced) from here.
- **Generic**: Reset and/or normalize styles, box-sizing definition, etc.
- **Elements**: Styling for bare HTML elements (like H1, A, etc.). These come with default styling from the browser
 so we can redefine them here.
- **Objects**: Class-based selectors which define undecorated design patterns like buttons and grids.
- **Components**: Specific UI components. UI components are often composed of Objects and Components.
- **Utilities**: Utilities and helper classes with ability to override anything which goes before in the triangle, eg.
 states like hidden.

### [**BEM**](http://getbem.com/naming/: Translating the Architectural principles into a methodology
Writing immutable, self documenting CSS can be done with methodologies like OOCSS, SMACSS or BEM. But only BEM can
 be used for a namespaced convention with low specificity and non generic selectors (like .active). Please read the
 BEM methodology carefully. It's simple and clear and doesn't need much explanation here.


Useful literature
-----------------
- [How browsers work: behind the scenes of modern web browsers](https://www.html5rocks.com/en/tutorials/internals/howbrowserswork)
- [BEM Methodology](https://en.bem.info/methodology/)


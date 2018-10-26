CSS Architecture
================

Architectural principles
------------------------

- The UI-design principles(language) and CSS naming share a common structure
- Mobile first, so the device with smallest screen has less css parsing
- [Use immutable css objects](https://csswizardry.com/2015/03/immutable-css/)
- [Single responsibility principle](https://en.wikipedia.org/wiki/Single_responsibility_principle)
- Components have there own namespace so they can be refactored
- Use predictable CSS rules
- CSS must be self documenting
- Keep the [specificity](https://css-tricks.com/specifics-on-css-specificity/) at 0,0,1,0 or 0,0,0,1
- Max dept of applicability: 1

Tools and methodologies
-----------------------

### Atomic design
To establish a common ground with the other UX people (UI designers/Interaction specialists/etc) Atomic design has
 been introduced. Atomic design forces the team to break the design up into reusable parts. This reduces the amount
  of redundancy and delivers reusable UI bits and pieces in a library composed of atoms, molecules and organisms.
  Those CSS declarations will be developed and provisioned on a seperate component library project and referenced in
  other frontend projects.

### Translating to a CSS Structure
Atomic design is a design principle which gives us an effective pattern library. This library can be used in a
 css structure. The main goal of a good CSS structure is to support with css specifics like namespacing, cascading and
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

### [**BEM**](https://en.bem.info/methodology/): Translating the Architectural principles into a methodology
Writing immutable, self documenting CSS can be done with methodologies like OOCSS, SMACSS or BEM. But only BEM for can
 be used for a namespaced convention with low specificity and non generic selectors (like .active). Please read the
 BEM methodology carefully. It's simple and clear and doesn't need much explanation here.

Because BEM and Atomic design are combined there is an extra layer required to store our Atoms, Molecules, and
 Organisms in the standard ITCSS layers. While doing this, we can remove the Objects layer, because we use Atoms as
  the smallest UI pattern and those will include design. The combined structure will look like:

 - Settings
 - Tools
 - Generic
 - Elements
 - **Atomic\Atoms**: UI elements that can't be broken down any further and serve as the elemental building blocks of an
  interface.
 - **Atomic\Molecules**: Collections of atoms that form relatively simple UI components
 - **Atomic\Organisms**: Complex components that form discrete sections of an interface that have a stand alone function
 - **Components**: Specific UI components, they do not define its own styles but @extend Molecules and Organisms
  into the component (BEM) namespace.
 - Utilities

Others notes
------------

### Living architecture
The final project goals are not very clear at this moment. So this will be a living document. Specifications will be
 added as the project grows.

Useful literature
-----------------
- [Atomic design](http://atomicdesign.bradfrost.com/)
- [How browsers work: behind the scenes of modern web browsers](https://www.html5rocks.com/en/tutorials/internals/howbrowserswork)
- [BEM Methodology](https://en.bem.info/methodology/)


# Meta
This repository is used to document and define coding practices such as coding styles, writing commit messages and documentation.

The code_conventions.md defines the general coding conventions, without going into language specifics. It is possible that certain languages have their own coding standards. If this is the case, an additional document is added, which provides addendums or changes to the general codestyle.

Vocabulary
---
 Solution for hotend versus nozzle and {}_index versus {}_nr or {}_number name usage:

 * Only use 'hotend'
 * Only use 'nozzle' to refer to (attributes of) the Olsson block at the end of the hotend
 * Perform renaming according to the Boy-scout Rule, only in the same(/smallest) scope as where changes are made.
 * Only use '{}_index' indicating an index, counting value, starting at zero (0), referring to a position in an iterable. This will mostly be the case.
 * Only use '{}_number' indicating a counting value, starting at one (1), referring to a ordinal number (e.g. first, second, third) nearly always used for communication to a user.

# Meta
Ultimaker common stuff, utils, codestyles and everything else that needs a home.

Here we define our meta-things for Ultimaker projects.

Vocabulary
---
 Solution for hotend versus nozzle and {}_index versus {}_nr or {}_number name usage:

 * Only use 'hotend'
 * Only use 'nozzle' to refer to (attributes of) the Olsson block at the end of the hotend
 * Perform renaming according to the Boy-scout Rule, only in the same(/smallest) scope as where changes are made.
 * Only use '{}_index' indicating an index, counting value, starting at zero (0), referring to a position in an iterable. This will mostly be the case.
 * Only use '{}_number' indicating a counting value, starting at one (1), referring to a ordinal number (e.g. first, second, third) nearly always used for communication to a user.

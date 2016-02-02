Writing proper commits
======================

This document started out with a lot of text as the why, what and how
to write proper commits. Once starting some doing some extra research
to find some other potentially missing or interesting bits and pieces
I stumbled upon this great document of XKCD's Chris Beams. This
document covered everything that was intended to end up in this text
and did it better. Because of this, that document is a required read.

http://chris.beams.io/posts/git-commit/

Linking Issues
--------------
As mentioned in the article, it is also possible to link issues to
commit messages. In our case, we use Jira as an issue tracker. To
link for example a Cura issue number 123, the string 'CURA-123' needs
to be mentioned in the commit message. For an Embedded issue 42, EM-42
needs to be added to the commit message.

TODO (needs discussion)
-----------------------
Signed-off-by: Transfer ownership
Reviewed-by: Should we use this method in the future?
Acked-by: Approved/Accepted/Acknowledged; possibly useful for contributions

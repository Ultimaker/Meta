Writing proper commits
======================

Ultimaker is not the first, only or last company to say something about how to work with git and commits. We do feel that commits are a vital part of software development.

In order to ensure that a basic know-how of how to properly do good commits, we find that all software engineers MUST read the following document and SHOULD adhere to it as much as possible;
http://chris.beams.io/posts/git-commit/

Linking Issues
--------------
All issue tracking within Ultimaker is done by using our Jira tracker. Since we have Jira setup in such a way that commits can be attributed to a specific issue, all commits made towards fixing / implementing a Jira ticket MUST be linked.

These tags, which take the form of `CURA-123` or `EM-42`, SHOULD be placed in the body of the commit message in order to prevent clutter in the summary.

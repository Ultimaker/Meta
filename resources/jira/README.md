Not everything can be done in Jira, for example counting all the assigned storypoint for a particular backlog.
The `backlog-overview.py` script creates an overview of detail information from a backlog export from Jira.

# How to use
Go to, in the sidebar, `Issues` > `View all issues and filters`.
Make sure the view contains the columns `Issue Type`, `Labels`, `Status` and `Story Points` (custom field).
Export as CVS, with semi-colon (;) separated.

```
$ python3 backlog-overview.py [EXPORTED_FILE_NAME].csv
```

The script will output the following details to std-out:
* Number of items per found ticket state

For everything that is not `Done` or `Rejected`:
* All used labels with a counter
* Number of bugs, new features and tasks
* Number of items labeled `TO_REFINE`
* Total amount of story points

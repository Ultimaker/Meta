# Jira Resources
A set of (Python) script to automate JIRA related tasks, reporting and/or monitoring.
Not everything can be done in Jira, for example counting all the assigned storypoint for a particular backlog.

## Requesting an API key
Go to `https://id.atlassian.com/manage-profile/security/api-tokens` to request an API token you need to execute the scripts in this directory.
The `JIRA_API_USR` key value is the e-mail address you use to sign in wiht Jira.

## Days In Sprint
The `days_in_sprint.py` script records snapshots of the current lane a ticket is in for an active sprint.
The results are writen to a csv file and appended to with every execution of the script.
This can help to analyze team behavior with regard to handling tickets in a sprint.

To execute:
```
JIRA_API_KEY=[JIRA_API_KEY] JIRA_API_USR=[JIRA_API_USER] BOARD_ID=[PROJECT_ID] ./days_in_sprint.py
```

The `BOARD_ID` is a Jira, project specific, board ID. This can be found in the URL of the sprint board, e.g.:
```
https://ultimaker.atlassian.net/jira/software/c/projects/MISP/boards/31
```

Where the project ID is `MISP` and the board id is `31`.

The `nodered_flows.json` is a NodeRed flow, automating the execution of the script every work day on 08:00 and sends an export of the graph via mail.
The flow expects the same environment variables as the script and also requires a password for sending the report by mail.
The flow also creates the python script on the file system, so it's fully autonomous and no additional actions are required to enable the flow.

## Backlog overview API
The `backlog-overview_api.py` script provides a highover overview of the **entire** backlog of a project (excluding *epics* and *tests*).

To execute:
```
JIRA_API_KEY=[JIRA_API_KEY] JIRA_API_USR=[JIRA_API_USER] PRJ_ID=[PROJECT_ID]./backlog-overview_api.py
```

The main data that is taken from the output of this script is the amount of...:
* tickets per label used
* bugs, features and tasks
* items to refine (labeled `TO_REFINE`)
* open tickets (not *done* or *rejected*)
* storypoints assigned to open tickets.

## Backlog overview
This is the *manual* version of the previous script and requires an export of Jira tickets from a project.

### How to use
In Jira, go to (in the sidebar) `Issues` > `View all issues and filters`.
Make sure the view contains the columns `Issue Type`, `Labels`, `Status` and `Story Points` (custom field).
Export as CVS, with semi-colon (;) separated.

```
$ python3 backlog-overview.py [EXPORTED_FILE_NAME].csv
```


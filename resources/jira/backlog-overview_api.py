import os

from jiraSDK import JiraSDK
from jira_report import JiraReport

api_key = os.environ.get("JIRA_API_KEY", "")
api_usr = os.environ.get("JIRA_API_USR", "")
prj_id = os.environ.get("JIRA_PRJ_ID", "")

js = JiraSDK(api_key, api_usr)
jira_report = JiraReport(js, prj_id)
jira_report.create()

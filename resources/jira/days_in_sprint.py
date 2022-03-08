import os

from progress_monitor import ProgressMonitor
from jiraSDK import JiraSDK

api_key = os.environ.get("JIRA_API_KEY", "")
api_usr = os.environ.get("JIRA_API_USR", "")
bid = int(os.environ.get("JIRA_BOARD_ID", 0))

js = JiraSDK(api_key, api_usr)
pm = ProgressMonitor(js, bid)

data_frames, sprints = pm.monitor_days_in_active_sprints(pm.board_id)
pm.graph_days(data_frames, sprints)
pm.export_graph("days_in_sprint.png")
pm.show_graph()

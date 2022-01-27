from collections import defaultdict
from typing import Dict, List, Tuple, Union
import os
from datetime import date

from jira.resources import Issue, Sprint
import pandas
import matplotlib.pyplot as plt

from jiraSDK import JiraSDK
from slackSDK import SlackSDK


class ProgressMonitor:
    DEFAULT_LANE = -1  # See lut: not in sprint

    lut = {"not in sprint": -1, "new": 0, "todo": 1, "in progress": 2, "review": 3, "ready for qa": 4, "done": 5}

    def __init__(self, jira_sdk, board_id: int) -> None:
        self._jira_sdk = jira_sdk
        self.board_id = board_id

    def get_issues_for_sprint(self, sprint_id: int) -> List[Issue]:
        return self._jira_sdk.grab_issues(f"Sprint={sprint_id}")

    def read_dataframe(self, sprint_id: int) -> pandas.DataFrame:
        file_name = f"{sprint_id}_monitor.csv"

        if os.path.exists(file_name):
            return pandas.read_csv(file_name, index_col=0, header=0).fillna(self.DEFAULT_LANE)

        return pandas.DataFrame(columns=["date"]).fillna(self.DEFAULT_LANE)

    def write_dataframe(self, sprint_id: int, data_frame: pandas.DataFrame) -> None:
        file_name = f"{sprint_id}_monitor.csv"
        data_frame.to_csv(file_name)
        os.sync()

    def get_issues_for_project(self, project_id: int) -> List[Issue]:
        jql = f"project = {project_id} AND type not in (Test)"
        return self._jira_sdk.grab_issues(jql)

    def monitor_days_in_sprint(self, sprint: Sprint) -> pandas.DataFrame:
        print(f"Monitoring days in sprint: ({sprint.id}) '{sprint.name}'")
        issues = self.get_issues_for_sprint(sprint.id)

        data_frame = self.read_dataframe(sprint.id)

        today = str(date.today())
        row: Dict[str, Union[str, int]] = {"date": today}
        print(f"({today}) Tickets in sprint:")

        for issue in issues[1:]:
            print(f"\t({issue.key}) '{issue.fields.summary}'")

            status = self.lut.get(issue.fields.status.name.lower(), -1)

            if status == -1:
                print(f"Unknown state '{issue.fields.status.name}'")

            row[issue.key] = status

        data_frame = data_frame.append(row, ignore_index=True).fillna(self.DEFAULT_LANE)
        # self.write_dataframe(sprint.id, data_frame)
        return data_frame

    def monitor_days_in_active_sprints(self, board_id: int) -> Tuple[pandas.DataFrame, Sprint]:
        sprints = self._jira_sdk.get_sprints(board_id, "active")
        sprint = sprints[0]

        return (self.monitor_days_in_sprint(sprint), sprint)

    def graph_days_in_sprint(self, data_frame: pandas.DataFrame) -> None:
        ax = data_frame.plot(marker="o")
        ax.get_legend().remove()

        y_values = list(self.lut.keys())
        y_labels = list(self.lut.values())

        x_values = list(data_frame["date"])
        x_labels = range(0, len(list(data_frame["date"])))

        # self._annotate_with_ticket_ids(ax, data_frame, x_labels)
        self._annotate_with_ticket_count(ax, data_frame, x_labels)

        plt.yticks(y_labels, y_values)
        plt.xticks(x_labels, x_values, rotation=45)

    def _annotate_with_ticket_count(self, ax, data_frame, x_labels) -> None:
        df_ticket_count = df.drop("date", 1).apply(pandas.Series.value_counts, axis=1).fillna(0)
        columns = data_frame.columns.values[1:]

        for x in x_labels:
            for col in columns:
                y = data_frame[col][x]

                ax.annotate(
                    f"[{int(df_ticket_count[y][x])}]",
                    (x, y),
                    textcoords="offset points",
                    xytext=(5, 5),
                )

    def _annotate_with_ticket_ids(self, ax, data_frame, x_labels) -> None:
        columns = data_frame.columns.values[1:]

        for x in x_labels:
            label_jump: Dict[int, int] = defaultdict(lambda: 1)
            for col in columns:
                y = data_frame[col][x]

                ax.annotate(
                    col[5:],
                    (x, y),
                    textcoords="offset points",
                    xytext=(10, 10 * label_jump[y]),
                )

                label_jump[y] += 1

    def show_graph(self) -> None:
        plt.show()

    def export_graph(self, file_name: str) -> None:
        plt.savefig(file_name, dpi=300)


# ---
api_key = os.environ.get("JIRA_API_KEY", "")
api_usr = os.environ.get("JIRA_API_USR", "")
bid = int(os.environ.get("JIRA_BOARD_ID", 0))

js = JiraSDK(api_key, api_usr)
pm = ProgressMonitor(js, bid)

df, s = pm.monitor_days_in_active_sprints(pm.board_id)
pm.graph_days_in_sprint(df)
fn = f"days_in_{s.id}.png"
pm.export_graph(fn)
# pm.show_graph()

# ---
channel_id = os.environ.get("SLACK_CHANNEL_ID", "")
app_token = os.environ.get("SLACK_BOT_TOKEN", "")

slack_sdk = SlackSDK(app_token, channel_id)
slack_sdk.send_file(fn, "HELLOE!")

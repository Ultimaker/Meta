from collections import defaultdict
import os
import time
from typing import Any, Dict, List, Tuple, Union

from jira.resources import Issue, Sprint
import matplotlib.pyplot as plt
import pandas

from jiraSDK import JiraSDK


class ProgressMonitor:
    DEFAULT_LANE = -1  # See lut: not in sprint
    SHIFT_DISTANCE = 0.06  # factor of plot height.

    lut = {"not in sprint": -1, "new": 0, "todo": 1, "in progress": 2, "review": 3, "ready for qa": 4, "done": 5}

    def __init__(self, jira_sdk: JiraSDK, board_id: int) -> None:
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
        data_frame = self.read_dataframe(sprint.id)
        issues = self.get_issues_for_sprint(sprint.id)

        today = time.strftime("%m/%d %H:%M", time.localtime())

        row: Dict[str, Union[str, int]] = {"date": today}
        print(f"({today}) Tickets in sprint:")

        for issue in issues[1:]:
            print(f"\t({issue.key}) '{issue.fields.summary}'")

            status = self.lut.get(issue.fields.status.name.lower(), -1)

            if status == -1:
                print(f"Unknown state '{issue.fields.status.name}'")

            row[issue.key] = status

        data_frame = data_frame.append(row, ignore_index=True).fillna(self.DEFAULT_LANE)
        self.write_dataframe(sprint.id, data_frame)
        return data_frame

    def monitor_days_in_active_sprints(self, board_id: int) -> Tuple[pandas.DataFrame, Sprint]:
        sprints = self._jira_sdk.get_sprints(board_id, "active")
        sprint = sprints[0]

        return (self.monitor_days_in_sprint(sprint), sprint)

    def graph_days_in_sprint(self, data_frame: pandas.DataFrame) -> None:
        ax = plt.subplot()

        # For other color maps, see: https://matplotlib.org/stable/tutorials/colors/colormaps.html
        ax.set_prop_cycle(plt.cycler("color", plt.cm.tab20.colors))

        y_values = list(self.lut.keys())
        y_labels = list(self.lut.values())

        x_values = list(data_frame["date"])
        x_labels = range(0, len(list(data_frame["date"])))

        idx: Dict[Tuple[int, Any], int] = defaultdict(lambda: 0)

        for name, values in data_frame.set_index("date").iteritems():
            # Some ranges have close lying colors, using the following loop,
            # forces the color cycler to use a more different color:
            # for x in range(15):
            #     ax._get_lines.get_next_color()

            # For a regular plot, with overlapping lines, use:
            # ax.plot(x_labels, values, marker='o', label=name, transform=trans3)

            # Shift data points:
            for x, value in enumerate(values):
                shift = idx[(x_labels[x], value)]
                values[x] += shift * self.SHIFT_DISTANCE
                idx[(x_labels[x], value)] += 1

            ax.plot(x_labels, values, label=name)

        plt.grid(True)

        # Show ticket labels at datapoints:
        # self._annotate_with_ticket_ids(ax, data_frame, x_labels)

        # Show ticket count at datapoints:
        # self._annotate_with_ticket_count(ax, data_frame, x_labels)

        plt.yticks(y_labels, y_values)
        plt.xticks(x_labels, x_values, rotation=45)

        plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left", borderaxespad=0)

    def _annotate_with_ticket_count(self, ax, data_frame, x_labels) -> None:
        df_ticket_count = data_frame.drop("date", axis=1).apply(pandas.Series.value_counts, axis=1).fillna(0)
        columns = data_frame.columns.values[1:]

        for x in x_labels:
            for col in columns:
                y = data_frame[col][x]

                ax.annotate(
                    f"[{int(df_ticket_count[y][x])}]",
                    (x, y),
                    textcoords="offset points",
                    xytext=(5, 5),
                    color="lightgrey",
                    size=8
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
        plt.savefig(file_name, dpi=300, bbox_inches='tight')

from collections import defaultdict
from datetime import datetime
import os
from typing import Any, Dict, List, Tuple, Union

import matplotlib.pyplot as plt
import pandas

from jnra.jiraSDK import JiraSDK
from jira.resources import Issue, Sprint


class ProgressMonitor:
    DEFAULT_LANE = 0  # See state_labels: not in sprint
    SHIFT_DISTANCE = 0.06  # factor of plot height.
    DATETIME_FORMAT = "%Y/%m/%d %H:%M"
    DPI = 300
    WEEKDAYS = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]

    state_labels = {"Not In Sprint": DEFAULT_LANE, "Todo": 1, "In Progress": 2, "Review": 3, "QA": 4, "Done": 5}
    lookup_states = {
        "not in sprint": DEFAULT_LANE,
        "new": 1, "todo": 1,  # States 'new' and 'todo' are handled the same
        "in progress": 2,
        "review": 3,
        "ready for qa": 4,
        "done": 5
    }

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

    def monitor_days(self, sprints: List[Sprint]) -> List[pandas.DataFrame]:
        sprint_frames: List[pandas.DataFrame] = []

        for sprint in sprints:
            sprint_frames.append(self._monitor_days_in_sprint(sprint))

        return sprint_frames

    def _monitor_days_in_sprint(self, sprint: Sprint) -> pandas.DataFrame:
        print(f"Monitoring days in sprint: ({sprint.id}) '{sprint.name}'")
        data_frame = self.read_dataframe(sprint.id)
        issues = self.get_issues_for_sprint(sprint.id)

        today = datetime.today().strftime(self.DATETIME_FORMAT)

        row: Dict[str, Union[str, int]] = {"date": today}
        print(f"({today}) Tickets in sprint:")

        for issue in issues[1:]:
            print(f"\t({issue.key}) '{issue.fields.summary}'")

            status = self.lookup_states.get(issue.fields.status.name.lower(), -1)

            if status == -1:
                print(f"Unknown state '{issue.fields.status.name}'")

            row[issue.key] = status

        data_frame = data_frame.append(row, ignore_index=True).fillna(self.DEFAULT_LANE)
        self.write_dataframe(sprint.id, data_frame)
        return data_frame

    def monitor_days_in_active_sprints(self, board_id: int) -> Tuple[List[pandas.DataFrame], List[Sprint]]:
        sprints = self._jira_sdk.get_sprints(board_id, "active")
        return (self.monitor_days(sprints), sprints)

    def graph_days(self, data_frames: List[pandas.DataFrame], sprints: List[Sprint]) -> None:
        _fig, ax = plt.subplots(
            1, len(data_frames),
            sharey='all',
            figsize=(18, 10)  # [inch]
        )
        plt.subplots_adjust(wspace = 0.05)
        plt.rcParams["font.family"] = "monospace"

        for idx, data_frame in enumerate(data_frames):
            ax[idx].set_title(f"({sprints[idx].id}) '{sprints[idx].name}'")
            self._graph_days_in_sprint(data_frame, ax[idx])

    def _graph_days_in_sprint(self, data_frame: pandas.DataFrame, ax: plt.Axes) -> None:
        y_labels = list(self.state_labels.keys())
        y_values = list(self.state_labels.values())

        x_labels = list(data_frame["date"])
        x_values = range(0, len(list(data_frame["date"])))

        # For other color maps, see: https://matplotlib.org/stable/tutorials/colors/colormaps.html
        ax.set_prop_cycle(plt.cycler("color", plt.cm.tab20.colors))

        idx: Dict[Tuple[int, Any], int] = defaultdict(lambda: 0)

        for name, values in data_frame.set_index("date").iteritems():
            # Some ranges have close lying colors, using the following loop,
            # forces the color cycler to use a more different color:
            # for x in range(15):
            #     ax._get_lines.get_next_color()

            # For a regular plot, with overlapping lines, use:
            # ax.plot(x_values, values, marker='o', label=name, transform=trans3)

            # Shift data points:
            for x, value in enumerate(values):
                shift = idx[(x_values[x], value)]
                values[x] += shift * self.SHIFT_DISTANCE
                idx[(x_values[x], value)] += 1

            ax.plot(x_values, values, marker='.', label=name)

        ax.grid(True)

        # Show ticket labels at datapoints:
        # self._annotate_with_ticket_ids(ax, data_frame, x_values)

        # Show ticket count at datapoints:
        # self._annotate_with_ticket_count(ax, data_frame, x_values)

        ax.set_yticks(y_values)
        ax.set_yticklabels(y_labels)

        ax.set_xticks(x_values)

        x_labels = self._dates_to_weekday(x_labels)
        ax.set_xticklabels(x_labels, rotation=45)

        ax.legend(loc="upper left", facecolor='white', framealpha=1)

    def _dates_to_weekday(self, values: List[str]) -> List[str]:
        weekdays: List[str] = []

        for day in values:
            tm = datetime.strptime(day, self.DATETIME_FORMAT)
            weekdays.append(self.WEEKDAYS[tm.weekday()])

        return weekdays

    def _annotate_with_ticket_count(
            self,
            ax: plt.Axes,
            data_frame: pandas.DataFrame,
            x_values: List[float]
    ) -> None:
        df_ticket_count = data_frame.drop("date", axis=1).apply(pandas.Series.value_counts, axis=1).fillna(0)
        columns = data_frame.columns.values[1:]

        for x in x_values:
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

    def _annotate_with_ticket_ids(
            self,
            ax: plt.Axes,
            data_frame: pandas.DataFrame,
            x_values: List[float]
    ) -> None:
        columns = data_frame.columns.values[1:]

        for x in x_values:
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

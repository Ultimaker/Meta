from collections import defaultdict
from typing import Dict, List, Tuple, Union
import os
from datetime import date

from pandas import DataFrame, read_csv

import matplotlib.pyplot as plt

from jira import JIRA
from jira.resources import Issue, Sprint, Board
from jira.client import ResultList

lut = {
    "new": 0,
    "todo": 1,
    "in progress": 2,
    "review": 3,
    "ready for qa": 4,
    "done": 5
}

api_key = os.environ.get("API_KEY", "")
api_user = os.environ.get("API_USR", "")
prj_id = int(os.environ.get("PRJ", 0))

jira = JIRA(
    'https://ultimaker.atlassian.net/',
    basic_auth=(api_user, api_key)
)

PAGE_SIZE = 50


class ProgressMonitor():

    def get_boards(self, project_id: str) -> List[Board]:
        boards = []
        total_boards = 1
        num_boards = 0

        while num_boards < total_boards:
            all_boards: ResultList[Board] = jira.boards(
                startAt=num_boards,
                maxResults=PAGE_SIZE,
                projectKeyOrID=project_id
            )

            for board in all_boards:
                boards.append(board)

            num_boards += len(all_boards)
            total_boards = all_boards.total

        print(f"Found '{len(boards)}' boards")
        for board in boards:
            print(f"\t({board.id}) '{board.name}'")

    def get_sprints(self, board_id: int, state: str) -> List[Sprint]:
        # sprint states:  future, active, closed
        sprints = []
        total_sprints = 1
        num_sprints = 0

        while num_sprints < total_sprints:
            all_sprints: ResultList[Sprint] = jira.sprints(
                board_id=board_id,
                startAt=num_sprints,
                maxResults=PAGE_SIZE,
                state=state
            )

            for sprint in all_sprints:
                sprints.append(sprint)

            num_sprints += len(all_sprints)
            total_sprints = all_sprints.total

        print(f"Found {len(sprints)} '{state}' sprints:")
        for sprint in sprints:
            print(f"\t({sprint.id}) '{sprint.name}'")

        return sprints

    def _grab_issues(self, jql: str) -> List[Issue]:
        num_issues = 0
        total = 1
        issues = []

        while num_issues < total:
            all_issues: ResultList[Issue] = jira.search_issues(
                jql,
                startAt=num_issues,
                maxResults=PAGE_SIZE
            )

            for issue in all_issues:
                issues.append(issue)

            num_issues += len(all_issues)
            total = all_issues.total

        return issues

    def get_issues_for_sprint(self, sprint_id: int) -> List[Issue]:
        return self._grab_issues(f"Sprint={sprint_id}")

    def read_dataframe(self, sprint_id: int) -> DataFrame:
        file_name = f"{sprint_id}_monitor.csv"

        if os.path.exists(file_name):
            return read_csv(file_name, index_col=0, header=0)

        return DataFrame(columns=["date"])

    def write_dataframe(self, sprint_id: int, data_frame: DataFrame) -> None:
        file_name = f"{sprint_id}_monitor.csv"
        data_frame.to_csv(file_name)
        os.sync()

    def get_issues_for_project(self, project_id: int) -> List[Issue]:
        jql = f"project = {project_id} AND type not in (Test)"
        return self._grab_issues(jql)

    def monitor_days_in_sprint(self, sprint: Sprint) -> DataFrame:
        print(f"Monitoring days in sprint: ({sprint.id}) '{sprint.name}'")
        issues = self.get_issues_for_sprint(sprint.id)

        data_frame = self.read_dataframe(sprint.id)

        today = str(date.today())
        row: Dict[str, Union[str, int]] = {"date": today}
        print(f"({today}) Tickets in sprint:")

        for issue in issues[1:]:
            print(f"\t({issue.key}) '{issue.fields.summary}'")

            status = lut.get(issue.fields.status.name.lower(), -1)

            if status == -1:
                print(f"Unknown state '{issue.fields.status.name}'")

            row[issue.key] = status

        data_frame = data_frame.append(row, ignore_index=True)
        self.write_dataframe(sprint.id, data_frame)
        return data_frame

    def monitor_days_in_active_sprints(self, project_id: int) -> Tuple[DataFrame, Sprint]:
        sprints = self.get_sprints(project_id, "active")

        for sprint in sprints:
            return (self.monitor_days_in_sprint(sprint), sprint)

    def graph_days_in_sprint(self, data_frame: DataFrame) -> None:
        ax = data_frame.plot(marker='o')
        ax.get_legend().remove()

        y_values = list(lut.keys())
        y_labels = list(lut.values())

        x_values = list(data_frame["date"])
        x_labels = range(0, len(list(data_frame["date"])))

        columns = data_frame.columns.values[1:]

        for x in x_labels:
            label_jump: Dict[int, int] = defaultdict(lambda: 1)
            for col in columns:
                y = data_frame[col][x]

                ax.annotate(
                    col[5:],
                    (x, y),
                    textcoords='offset points',
                    xytext=(10, 10*label_jump[y]),
                )

                label_jump[y] += 1

        plt.yticks(y_labels, y_values)
        plt.xticks(x_labels, x_values)

    def show_graph(self) -> None:
        plt.show()

    def export_graph(self, file_id: str) -> None:
        plt.savefig(f"{file_id}.png", dpi=300)


# ---
pm = ProgressMonitor()
df, s = pm.monitor_days_in_active_sprints(prj_id)
pm.graph_days_in_sprint(df)
pm.export_graph(f"days_in_{s.id}")
pm.show_graph()

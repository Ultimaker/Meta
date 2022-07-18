from typing import List

from jira import JIRA
from jira.resources import Issue, Board, Sprint
from jira.client import ResultList


class JiraSDK():

    PAGE_SIZE = 50

    def __init__(self, api_key: str, api_usr: str) -> None:
        self._jira = JIRA("https://ultimaker.atlassian.net/", basic_auth=(api_usr, api_key))

    def get_boards(self, project_id: str) -> List[Board]:
        boards = []
        total_boards = 1
        num_boards = 0

        while num_boards < total_boards:
            all_boards: ResultList[Board] = self._jira.boards(
                startAt=num_boards, maxResults=self.PAGE_SIZE, projectKeyOrID=project_id
            )

            for board in all_boards:
                boards.append(board)

            num_boards += len(all_boards)
            total_boards = all_boards.total

        print(f"Found {len(boards)} boards")
        for board in boards:
            print(f"\t({board.id}) '{board.name}'")

    def get_sprints(self, board_id: int, state: str) -> List[Sprint]:
        # sprint states:  future, active, closed
        sprints = []
        total_sprints = 1
        num_sprints = 0

        while num_sprints < total_sprints:
            all_sprints: ResultList[Sprint] = self._jira.sprints(
                board_id=board_id, startAt=num_sprints, maxResults=self.PAGE_SIZE, state=state
            )

            for sprint in all_sprints:
                sprints.append(sprint)

            num_sprints += len(all_sprints)
            total_sprints = all_sprints.total

        print(f"Found {len(sprints)} '{state}' sprints:")
        for sprint in sprints:
            print(f"\t({sprint.id}) '{sprint.name}'")


        return sprints

    def grab_issues(self, jql: str) -> List[Issue]:
        num_issues = 0
        total = 1
        issues = []

        while num_issues < total:
            print(f"Grabbing {num_issues}-{num_issues+self.PAGE_SIZE} ({total})")
            all_issues: ResultList[Issue] = self._jira.search_issues(
                jql, startAt=num_issues, maxResults=self.PAGE_SIZE
            )

            for issue in all_issues:
                issues.append(issue)

            num_issues += len(all_issues)
            total = all_issues.total

        print(f"Found {len(issues)}/{total} issues")
        return issues



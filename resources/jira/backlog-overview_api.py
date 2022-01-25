from collections import defaultdict
from typing import Dict, List
import os

from jira import JIRA
from jira.resources import Issue
from jira.client import ResultList


class JiraReport():

    def __init__(self) -> None:
        self._num_issues = 0
        self._total = 1
        self._issues: List[Issue] = []

        self._labels: Dict[str, int] = defaultdict(int)
        self._sp_count = 0.0

        self._types: Dict[str, int] = defaultdict(int)
        self._states: Dict[str, int] = defaultdict(int)
        self._page_size = 50

    def _grab_issues(self) -> None:
        api_key = os.environ.get("API_KEY", "")
        api_user = os.environ.get("API_USR", "")

        jira = JIRA(
            'https://ultimaker.atlassian.net/',
            basic_auth=(api_user, api_key)
        )

        while self._num_issues < self._total:
            print(f"Grabbing {self._num_issues}-{self._num_issues+self._page_size} ({self._total})")
            all_project_issues: ResultList[Issue] = jira.search_issues(
                'project = MISP',
                # 'AND type not in (Test, Epic) '
                # 'AND status in ("new", "todo", "in progress", "review", "ready for qa")',
                startAt=self._num_issues,
                maxResults=self._page_size
            )

            for issue in all_project_issues:
                self._issues.append(issue)

            self._num_issues += len(all_project_issues)
            self._total = all_project_issues.total

    def _log_findings(self) -> None:
        sorted_labels = list(self._labels.items())
        sorted_labels.sort(key=lambda i: -i[1])

        print("Labels:")
        for name, count in sorted_labels:
            print(f"\t{name or 'N.A'}: {count}")
        print("Types:")
        total_types = 0

        for name, count in self._types.items():
            print("\t%s: %s" % (name, count))
            total_types += count
        print("\tTOTAL %s" % total_types)

        print("States:")
        for name, count in self._states.items():
            print("\t%s: %s" % (name, count))

        print("To refine: %d" % self._labels["to_refine"])
        print("Total SP: %d" % self._sp_count)

    def _is_reject_type_2(self, issue: Issue) -> bool:
        issue_type = issue.fields.issuetype.name.lower()

        if issue_type in ("test", "epic"):
            return True

        self._types[issue_type] += 1

        return False

    def _is_reject_status_2(self, issue: Issue) -> bool:
        status = issue.fields.status.name.lower()  # line_elts[status_idx]
        self._states[status] += 1

        if status not in ("new", "todo", "in progress", "review", "ready for qa"):

            if status not in ("done", "rejected"):
                print(f"Ignored status [{status}] > {issue.key}")

            return True

        return False

    def _count_points_2(self, issue: Issue) -> None:
        self._sp_count += float(issue.fields.customfield_10028 or "0")

    def _count_labels_2(self, issue: Issue) -> None:
        for label in issue.fields.labels:
            label = label.lower()
            self._labels[label] += 1

    def create(self) -> None:
        self._grab_issues()

        for issue in self._issues:

            if self._is_reject_status_2(issue) or self._is_reject_type_2(issue):
                continue

            self._count_labels_2(issue)
            self._count_points_2(issue)

        self._log_findings()


jira_report = JiraReport()
jira_report.create()

for issue in jira_report._issues:
    json_ticket = json.dumps(issue.raw, indent=4)
    print(f"__ {json_ticket}")
    # print(f"{issue.fields.customfield_10028}")
    # break
    # print(f"__ {issue.fields.__dir__}")
    # print(f">>> {issue.fields.labels}")
    # for fld in issue.fields:
        # print(f"XX {fld}")

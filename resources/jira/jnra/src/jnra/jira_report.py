from collections import defaultdict
from typing import Dict

from jira.resources import Issue

from .jiraSDK import JiraSDK


class JiraReport:
    def __init__(self, jira_sdk: JiraSDK, project_id: str) -> None:
        self._labels: Dict[str, int] = defaultdict(int)
        self._sp_count = 0.0

        self._types: Dict[str, int] = defaultdict(int)
        self._states: Dict[str, int] = defaultdict(int)

        self._project_id = project_id
        self._jira_sdk = jira_sdk

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

    def _is_reject_type(self, issue: Issue) -> bool:
        issue_type = issue.fields.issuetype.name.lower()

        if issue_type in ("test", "epic"):
            return True

        self._types[issue_type] += 1

        return False

    def _is_reject_status(self, issue: Issue) -> bool:
        status = issue.fields.status.name.lower()  # line_elts[status_idx]
        self._states[status] += 1

        if status not in ("new", "todo", "in progress", "review", "ready for qa"):

            if status not in ("done", "rejected", "closed"):
                print(f"Ignored status [{status}] > {issue.key}")

            return True

        return False

    def _count_points(self, issue: Issue) -> None:
        self._sp_count += float(issue.fields.customfield_10028 or "0")

    def _count_labels(self, issue: Issue) -> None:
        for label in issue.fields.labels:
            label = label.lower()
            self._labels[label] += 1

    def create(self) -> None:
        all_project_issues = self._jira_sdk.grab_issues(
            f"project = {self._project_id}",
        )

        for issue in all_project_issues:

            if self._is_reject_status(issue) or self._is_reject_type(issue):
                continue

            self._count_labels(issue)
            self._count_points(issue)

        self._log_findings()

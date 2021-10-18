import sys
import os
from typing import List

from os import path
from collections import defaultdict

text = open(sys.argv[1]).read()
lines = text.split("\n")
labels = {}

label_idx = set()
sp_idx = None
status_idx = None
type_idx = None

sp_count = 0

types = defaultdict(int)
states = defaultdict(int)

def _is_reject_status(line_elts: List[str]) -> bool:
    status = line_elts[status_idx]
    states[status] += 1

    if status not in ("new", "todo", "in progress", "review", "ready for qa"):

        if status not in ("done", "rejected"):
            print(f"Ignored status [{status}] > {line}")

        return True

    return False

def _is_reject_type(line_elts: List[str]) -> bool:
    if type_idx is not None:
        ticket_type = line_elts[type_idx]

        if ticket_type in ("test", "epic"):
            return True

        types[ticket_type] += 1

    return False

def _count_labels(line_elts:List[str]) -> None:
    for idx in label_idx:
        try:
            label = line_elts[idx]
            if label not in labels:
                labels[label] = 0
            labels[label] += 1
        except:
            pass

def _count_points(line_elts: List[str]) -> None:
    if sp_idx is not None:
        global sp_count

        try:
            sp_count += float(line_elts[sp_idx] or "0")
        except Exception as ex:
            print("Fork:", repr(ex), " >> ", line_elts)

def _log_findings() -> None:
    sorted_labels = list(labels.items())
    sorted_labels.sort(key=lambda i: -i[1])

    print("Labels:")
    for name, count in sorted_labels:
        print(f"\t{name or 'N.A'}: {count}")
    print("Types:")
    for name, count in types.items():
        print("\t%s: %s" % (name, count))

    print("States:")
    for name, count in states.items():
        print("\t%s: %s" % (name, count))

    print("To refine: %d" % labels["to_refine"])
    print("Total SP: %d" % sp_count)

for idx, column_name in enumerate(lines[0].split(";")):
    if column_name == "Labels":
        label_idx.add(idx)
    if column_name == "Custom field (Story Points)":
        sp_idx = idx
    if column_name == "Status":
        status_idx = idx
    if column_name == "Issue Type":
        type_idx = idx

for line in lines[1:]:
    line = line.strip()

    if len(line) == 0:
        continue

    line_split = line.lower().split(";")

    if _is_reject_status(line_split) or _is_reject_type(line_split):
        continue

    _count_labels(line_split)
    _count_points(line_split)

_log_findings()

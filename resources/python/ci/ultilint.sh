#!/bin/sh

set -eu

USE_DUMMY_DBUS=true PYTHONPATH=:../dbus-interface-lib:../charon:../libSmeagol:../libsmeagol:../marvin-service/src:./ python3 scripts/util/lint_machine_definitions_to_python.py

exit 0

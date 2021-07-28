#!/bin/sh

set -eu

py3clean .
rm -rf ./.cache
rm -rf ./.pytest_cache
rm -rf ./.mypy_cache
rm -rf ./cov_report
USE_DUMMY_DBUS=true \
    PYTHONPATH=:../dbus-interface-lib:../libpalantir:../libPalantir:../charon:../libCharon:../libsmeagol:../libSmeagol:../marvin-service/src \
    pytest --cov=. --cov-report=html --cov-config=./coverage.ini
py3clean .

echo "Getting coverage report"

coverage report

exit 0

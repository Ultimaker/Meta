#!/bin/sh
. ci/references.sh

set -eu
# Log version to track if the non specified version has changed and is breaking stuff.
mypy -V

if [ -n "${CHANGED_FILES}" ]; then
    echo "Mypy testing for "
    echo "${CHANGED_FILES}"
    # Ignore shellcheck for variable without quotes
    # shellcheck disable=SC2086
    mypy --config-file=mypy.ini --follow-imports=skip --cache-dir=/dev/null ${CHANGED_FILES}
fi

exit 0
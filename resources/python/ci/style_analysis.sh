#!/bin/sh
. ci/references.sh

set -eu
# Log version to track if the non specified version has changed and is breaking stuff.
pycodestyle --version

if [ -n "${CHANGED_FILES}" ]; then
    echo "PyCodeStyle testing for"
    echo "${CHANGED_FILES}"
    # Ignore shellcheck for variable without quotes
    # shellcheck disable=SC2086
    pycodestyle --config=pycodestyle.ini ${CHANGED_FILES}
fi

exit 0
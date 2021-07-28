#!/bin/sh

set -eu

PARENT_BRANCH=${PARENT_BRANCH:-master}
CHANGED_BRANCH_FILES=$(git diff --name-only --diff-filter=d origin/"${PARENT_BRANCH}"...HEAD | grep -i .py$ | cat)
if [ -z "${ONLY_CHECK_STAGED:=""}" ] ; then
    echo "Local + staged + branch changes"
    CHANGED_LOCAL_FILES=$(git diff --name-only --diff-filter=d HEAD | grep -i .py$ | cat)
else
    echo "Staged + branch changes"
    CHANGED_LOCAL_FILES=$(git diff --name-only --diff-filter=d --staged | grep -i .py$ | cat)
fi
CHANGED_FILES=$(echo "${CHANGED_BRANCH_FILES}" "${CHANGED_LOCAL_FILES}" | tr ' ' '\n' | sort | uniq)

export CHANGED_FILES
#!/bin/sh

set -eu

. ./make_docker.sh

git fetch

run_in_docker "ci/flake8.sh" || echo "Failed!"

exit 0

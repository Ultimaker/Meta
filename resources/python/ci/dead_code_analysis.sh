#!/bin/sh

set -eu

vulture --min-confidence 95 "griffin"

exit 0

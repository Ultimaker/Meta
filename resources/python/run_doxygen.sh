#!/bin/bash


CONFIG_FILE="Doxyfile"
DOXYGEN_EXECUTABLE=$(command -v doxygen)
WC_EXECUTABLE=$(command -v wc)
LESS_EXECUTABLE=$(command -v less)

DOXYGEN_OUTPUT_FILE="/tmp/doxygen.txt"
DOXYGEN_WARNINGS_OUTPUT_FILE="/tmp/doxygen-warnings.txt"

###################
# Helper functions
###################

# Function that works like echo, but prints bold. Used to distinct between our output and output from tools we call.
info() {
    echo -e -n "\e[1m"
    echo -n "$*"
    echo -e "\e[0m"
}

# Function that works like echo, but prints in orange. Used to make the user notice a warning.
warn() {
    echo -e -n "\033[0;33m"
    echo -n "$*"
    echo -e "\e[0m"
}

# Function that works like echo, but prints in red. Used to make the user notice an error.
# This function will always exit!
error() {
    echo -e -n "\033[0;31m"
    echo -n "$*"
    echo -e "\e[0m"
    exit 1
}

main() {
  if [[ ! -f ${CONFIG_FILE} ]]; then
    error "Missing configuration file ${CONFIG_FILE}..."
  fi
 
  if [[ -z ${DOXYGEN_EXECUTABLE} ]]; then
    error "Cannot find doxygen executable. Please install doxygen first!"
  fi

  if [[ -z ${WC_EXECUTABLE} ]]; then
    error "Cannot find wc executable. Please install wc first!"
  fi

  if [[ -z ${LESS_EXECUTABLE} ]]; then
    error "Cannot find less executable. Please install less first!"
  fi

  info "Running doxygen... please wait..." 
  ${DOXYGEN_EXECUTABLE} 1>${DOXYGEN_OUTPUT_FILE} 2>${DOXYGEN_WARNINGS_OUTPUT_FILE}

  issue_count=$(${WC_EXECUTABLE} -l < ${DOXYGEN_WARNINGS_OUTPUT_FILE})
  if [[ ${issue_count} -gt 0 ]]; then
    warn "Doxygen encountered problems during generation:"
    ${LESS_EXECUTABLE} ${DOXYGEN_WARNINGS_OUTPUT_FILE}
  fi

  info "Finished"
}

main


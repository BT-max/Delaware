#!/bin/bash

# Check that at least one argument was provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <keyword>"
    exit 1
fi

# Extract the keyword from the first argument
keyword="$1"

# Run the pdfgrep command with the keyword
pdfgrep -A 1 -B 1 "$keyword" downloads/*.pdf -h

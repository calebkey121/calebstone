#!/bin/bash

# Create the 'claude' directory if it doesn't exist
mkdir -p claude

# Find and copy .py files excluding the 'archive' directory
find . -type d -name 'archive' -prune -o -type f -name '*.py' -exec cp '{}' claude/ \;

#!/bin/bash

# Create the 'context_files' directory if it doesn't exist
mkdir -p context_files

# Find and copy .py files excluding the 'archive' and 'tests' directories
find . \( -type d -name 'archive' -o -name 'tests' \) -prune -o -type f -name '*.py' -exec cp '{}' context_files/ \;

# Find and copy js/jsx/ts/tsx files from client directory
find ./client/src -type f \( -name '*.js' -o -name '*.jsx' -o -name '*.ts' -o -name '*.tsx' \) -exec cp '{}' context_files/ \;

# Run the generate_tree.py script
python3 generate_tree.py

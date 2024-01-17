#!/bin/bash

# Move to correct directory
repo_path="$(dirname "$0")"
cd "$repo_path"

# Activate the virtual environment
source /home/arcane/repos/ilol-ladder/venv/bin/activate

# Run the Python script
python /home/arcane/repos/ilol-ladder/app/main.py &
python_pid=$!

# Wait for the Python script to finish executing
wait $python_pid

# Check for errors in the Python script
if [ $? -eq 0 ]; then
    # Add all changed files
    git add .

    # Commit changes with the message "Refresh ladder"
    git commit -m "Refresh ladder"

    # Push changes to the remote repository
    git push
else
    echo "Python script failed to execute."
fi

deactivate

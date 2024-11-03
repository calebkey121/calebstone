import os

def generate_tree(dir_path=".", prefix="", ignore_extensions=None, ignore_folders=None, output_file="context_files/project_structure.txt"):
    if ignore_extensions is None:
        ignore_extensions = []
    if ignore_folders is None:
        ignore_folders = []

    # Initialize output with the introductory line
    output = ["This is the project file structure:\n"]

    def _generate_tree_recursive(dir_path, prefix):
        try:
            contents = sorted(os.listdir(dir_path))
        except PermissionError:
            output.append(f"{prefix} [Permission Denied]\n")
            return

        for index, item in enumerate(contents):
            path = os.path.join(dir_path, item)
            is_last = index == len(contents) - 1

            # Check if the item should be ignored based on its extension or folder name
            if os.path.isdir(path):
                if item in ignore_folders:
                    continue  # Skip this folder
                output.append(f"{prefix}{'└── ' if is_last else '├── '}{item}/\n")
                _generate_tree_recursive(path, prefix + ("    " if is_last else "│   "))
            else:
                if any(item.endswith(ext) for ext in ignore_extensions):
                    continue  # Skip this file
                output.append(f"{prefix}{'└── ' if is_last else '├── '}{item}\n")

    # Run the recursive function starting from the top directory
    _generate_tree_recursive(dir_path, prefix)

    # Write the output to a file
    with open(output_file, "w") as file:
        file.writelines(output)

# Usage
# Customize the lists below to ignore specific extensions and folders
ignore_extensions = [".pyc", ".log"]  # Add file extensions to ignore
ignore_folders = ["__pycache__", "node_modules", ".git", ".vscode", "art"]  # Add folder names to ignore

# Run the function, which will start from the current directory
generate_tree(ignore_extensions=ignore_extensions, ignore_folders=ignore_folders)

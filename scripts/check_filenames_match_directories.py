import os
import sys


# List of filenames to be excluded
EXCLUDED_FILENAMES = ["index", "datapackage", "context-short", "rules"]

# List of extensions to be excluded
EXCLUDED_EXTENSIONS = [".oas3.yaml", ".md", ".shacl", ".frame.yamlld", ".ld.yaml"]

def split_filename_extension(filename):
    """
    Split filename into name and extension.
    Args:
        filename (str): The filename to split.
    Returns:
        tuple: A tuple containing the name and extension of the filename.
    """
    parts = filename.split(".")
    if len(parts) > 2:
        # If there are more than 1 periods, consider the last one as part of the extension
        # e.g. education-level.frame.yamlld -> education-level .frame.yamlld
        name = ".".join(parts[:-2])
        extension = "." + ".".join(parts[-2:])
    else:
        # Otherwise, consider only the extension as the last part
        name, extension = os.path.splitext(filename)

    return name, extension

def check_filenames_match_directories(root_dirs):
    """
    Check if filenames match the containing directory names.
    Args:
        root_dirs (list): A list of root directories to be checked.
    Returns:
        bool: True if all filenames match their containing directory names, False otherwise.
    """

    for root_dir in root_dirs:
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                name, extension = split_filename_extension(filename)
                parent_dir = os.path.basename(dirpath)
                parent_dir_1 = os.path.basename(os.path.dirname(dirpath))
                parent_dir_2 = os.path.basename(os.path.dirname(os.path.dirname(dirpath)))
                if name != parent_dir and name != parent_dir_1 and name != parent_dir_2:
                    if name not in EXCLUDED_FILENAMES and extension not in EXCLUDED_EXTENSIONS:
                        print(f"Error: Filename '{filename}' in '{dirpath}' dir does not match its containing directory name.")
                        return False

    return True

def check_directory_existence(root_dirs):
    existing_dirs = [root_dir for root_dir in root_dirs if os.path.exists(root_dir)]

    if not existing_dirs:
        print(f"{root_dirs} don't exist")
        return False
    
    # Check if any directories don't exist
    non_existent_dirs = [root_dir for root_dir in root_dirs if root_dir not in existing_dirs]

    for root_dir in non_existent_dirs:
        print(f"WARNING: {root_dir} does not exist")
    return True

def main():
    root_dirs = sys.argv[1:]  # Read dir args

    if not root_dirs:
        print("No root directories provided.")
        exit(1)
        
    if not check_directory_existence(root_dirs):
        exit(1)

    if not check_filenames_match_directories(root_dirs):
        exit(1)

if __name__ == "__main__":
    main()


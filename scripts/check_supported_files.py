import os
import sys
from pathlib import Path

"""
This script checks the leaf directories of the specified root directories to ensure that each leaf directory contains at least one .ttl file in UTF-8 format.
"""

def is_utf8(file_path):
    """
    Check if a file is encoded in UTF-8 format.
    Args:
        file_path (str): The path to the file.
    Returns:
        bool: True if the file is encoded in UTF-8, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read()
        return True
    except UnicodeDecodeError:
        return False

def check_supported_files(root_dirs):
    """
    Check if the leaf directories contain at least one .ttl file in UTF-8 format.
    Args:
        root_dirs (list): A list of root directories to be checked.
    Returns:
        bool: True if all leaf directories contain a .ttl file in UTF-8 format, False otherwise.
    """
    def dfs(directory):
        """
        Perform a depth-first search (DFS) to check leaf directories.
        Args:
            directory (Path): The directory to be checked.
        Returns:
            bool: True if all leaf directories contain a .ttl file in UTF-8 format, False otherwise.
        """
        has_ttl_file = False
        if not any(item.is_dir() for item in directory.iterdir()):
            for item in directory.iterdir():
                if item.is_file() and item.suffix == '.ttl':
                    has_ttl_file = True
                    if not is_utf8(item):
                        print(f"Error: {item} is not encoded in UTF-8.")
                        return False
            if not has_ttl_file and directory != root_dir:
                print(f"Error: No .ttl files found in directory: {directory}")
                return False
        else:
            for item in directory.iterdir():
                if item.is_dir():
                    if not dfs(item):
                        return False

        return True

    for root_dir in root_dirs:
        root_path = Path(root_dir)
        if not root_path.exists() or not root_path.is_dir():
            print(f"Error: Invalid root directory: {root_dir}")
            return False

        if not dfs(root_path):
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
    root_dirs = sys.argv[1:]

    if not root_dirs:
        print("No root directories provided.")
        exit(1)
        
    if not check_directory_existence(root_dirs):
        exit(1)

    if not check_supported_files(root_dirs):
        exit(1)

if __name__ == "__main__":
    main()

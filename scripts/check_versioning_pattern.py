#!/usr/bin/env python
import sys
import os
import re

def check_versioning_pattern(root_dirs):
    """
    Check if the versioning pattern is correct for leaf directories.
    """
    version_pattern = r"(latest|v?\d+(\.\d+){0,2})$"  # Regular expression pattern to match versioning format
    dir_pattern = r"(latest|\b(?:\D*\d\D*)+\b)"  # Regular expression pattern to match directory names
    errors = False
    checked_versions = {}  # Dictionary to store checked versions

    for root_dir in root_dirs:
        for dirpath, dirnames, _ in os.walk(root_dir):

            if not dirnames:  # Check only leaf directories
                versions = set()
                for dirname in os.listdir(os.path.dirname(dirpath)):

                    if re.match(dir_pattern, dirname):  # Check if the directory name matches the pattern
                        versions.add(dirname)

                # Remove "latest" if present in the set
                versions.discard("latest")

                superior_directory_path = os.path.dirname(dirpath)

                # Check if the versions have already been checked
                if tuple(versions) in checked_versions:
                    continue  # Skip if already checked

                # Verify that all strings in the set start with a number or "v"
                if not (all(re.match(r"v\d", version) for version in versions) or all(version[0].isdigit() for version in versions)):
                    # If not all strings start with a number or "v", report an error
                    print(f"Error: Inconsistent versioning pattern found in {superior_directory_path}: {versions}")
                    errors = True

                # Verify that all strings in the set match the versioning pattern
                if not (all(re.match(version_pattern, version) for version in versions)):
                    print(f"Error: Inconsistent versioning pattern found in {superior_directory_path}: {versions}")
                    errors = True

                checked_versions[tuple(versions)] = True  # Mark versions as checked

    return not errors

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
    root_dirs = sys.argv[1:]  # Read args

    if not root_dirs:
        print("No root directories provided.")
        exit(1)
        
    if not check_directory_existence(root_dirs):
        exit(1)

    if not check_versioning_pattern(root_dirs):
        exit(1)

if __name__ == "__main__":
    main()

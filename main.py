"""
Hash My Files

A Python script to generate and verify SHA256 hashes for media files in a
directory.

Overview:
- This script provides functionality to generate SHA256 hashes for media files
  with specified extensions (e.g., '.mp4', '.mkv') in a given directory.
- It can verify files in the directory against previously generated hashes
  stored in an SQLite database.
- The script integrates with a database module for efficient hash storage.

Global Constants:
- MEDIA_EXTENSIONS: Tuple of media file extensions to
  consider for hash generation.
- BLOCK_SIZE: The block size used for reading file content
  during hash generation.
- DB_FILE: The default name of the SQLite database file for storing hashes.

Usage:
1. To generate hashes for media files in a directory:
    ```bash
    python3 main.py -g /path/to/directory
    ```

2. To verify files against stored hashes in a directory:
    ```bash
    python3 main.py -v /path/to/directory
    ```
"""
import os
import sys
import hashlib
import database

MEDIA_EXTENSIONS = (".mp4", ".mkv")
BLOCK_SIZE = 65536
DB_FILE = "hashmyfiles.db"


def find_files_with_extension(dir_path, extensions):
    """
    Find files with a specific extension in the given directory.

    Args:
        dir_path (str): The path to the directory.
        extensions (tuple): Tuple of file extensions to search for.

    Returns:
        list: List of file paths with the specified extensions.
    """
    files = []
    for root, _, files_list in os.walk(dir_path):
        for file in files_list:
            if file.endswith(extensions):
                files.append(os.path.join(root, file))
    return files


def generate_sha256_hash(file_path):
    """
    Generate SHA256 hash for a given file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: SHA256 hash of the file.
    """
    with open(file_path, "rb") as f:
        sha256 = hashlib.sha256()
        for block in iter(lambda: f.read(BLOCK_SIZE), b''):
            sha256.update(block)
        return sha256.hexdigest()


def generate(dir_path):
    """
    Generate SHA256 hashes for media files in the specified directory.

    Args:
        dir_path (str): Path to the directory containing media files.
    """
    if os.path.isdir(dir_path):
        db_file = os.path.join(dir_path, DB_FILE)

        if os.path.isfile(db_file):
            print(f"{db_file} exists. Will look for new files...\n")
        else:
            print(f"{db_file} does not exist. Creating a new database...\n")
            database.create_new_database(db_file)

        media_files = find_files_with_extension(dir_path, MEDIA_EXTENSIONS)

        for media_file in media_files:
            if not database.media_file_exist(db_file, media_file):
                print(f"Generate hash for: {media_file}")
                generated_hash = generate_sha256_hash(media_file)
                database.add_hash(db_file, media_file, generated_hash)

        print("Done")
        sys.exit(0)
    else:
        print(f"{dir_path} is not a directory")
        sys.exit(1)


def verify(dir_path):
    """
    Verify files in the specified directory against stored SHA256 hashes.

    Args:
        dir_path (str): Path to the directory containing files to be verified.
    """
    db_file = os.path.join(dir_path, DB_FILE)

    if not os.path.isfile(db_file):
        print(f"{db_file} does not exist. Please generate hashes first.")
        sys.exit(1)

    print(f"{db_file} exists. Verifying files...\n")
    db_hashes = database.get_hashes(db_file)
    corrupted_files = []

    for db_hash in db_hashes:
        media_file = db_hash[0]
        if not os.path.isfile(media_file):
            corrupted_files.append((media_file, db_hash[1], "File not found"))
            print(f"{media_file} [Corrupted]")
            continue
        generated_hash = generate_sha256_hash(media_file)

        if generated_hash == db_hash[1]:
            print(f"{media_file} [OK]")
        else:
            corrupted_files.append((media_file, db_hash[1], generated_hash))
            print(f"{media_file} [Corrupted]")

    if corrupted_files:
        print(f"\n{len(corrupted_files)} corrupted files:")
        for corrupted_file in corrupted_files:
            print(f"File: {corrupted_file[0]}")
            print(f"Expected hash: {corrupted_file[1]}")
            print(f"File hash: {corrupted_file[2]}\n")
        sys.exit(1)
    else:
        print("\nNo corrupted files found")
        sys.exit(0)


if __name__ == "__main__":
    try:
        args = sys.argv[1:]

        if len(args) < 2:
            print("Not enough arguments")
            sys.exit(1)

        option = args[0]
        directory = args[1]

        match option:
            case "-g":
                generate(directory)
            case "-v":
                verify(directory)
            case _:
                print("Invalid option")
                sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation interrupted. Exiting...")
        sys.exit(1)

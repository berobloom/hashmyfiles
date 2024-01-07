# Hash My Files

A Python script to generate and verify SHA256 hashes for media files in a directory.
I also use this in my personal setup.

## Overview

This script provides functionality to generate SHA256 hashes for media files with specified extensions (e.g., '.mp4', '.mkv') in a given directory. It can verify files in the directory against previously generated hashes stored in an SQLite database. The script integrates with a database module for efficient hash storage.

## Requirements

- Python 3.6 or higher
- SQLite

## Usage

### Generate Hashes

To generate hashes for media files in a directory, use the `-g` option followed by the path to the directory:

```bash
python3 hash_my_files.py -g /path/to/directory
```

# Verify Hashes

To verify files against stored hashes in a directory, use the -v option followed by the path to the directory:

```bash
python3 hash_my_files.py -v /path/to/directory
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This software is released under the [BOLA License](LICENSE).

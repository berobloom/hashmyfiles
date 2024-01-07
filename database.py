"""
Database Module

This module provides functions for interacting with an SQLite database,
including executing queries,
checking the existence of paths, getting a list of files, adding hashes,
and creating a new database.

Functions:
- `execute_query`: Execute a database query and handle transactions.
- `media_file_exist`: Check if a path exists in the database.
- `get_hashes`: Get a list of files in the database.
- `add_hash`: Add a hash to the database.
- `create_new_database`: Create a new database.

Each function has its own docstring describing its purpose, arguments,
and return values.
"""

import sqlite3


def execute_query(db_file, query, parameters=None):
    """
    Execute a database query and handle transactions.

    Args:
        db_file (str): Path to the SQLite database file.
        query (str): SQL query to be executed.
        parameters (tuple): Parameters for the query.

    Returns:
        Any: Result of the query.
    """
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            result = (
                cursor.fetchall()
                if query.lower().startswith("select")
                else None
            )
            conn.commit()
            return result
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None


def media_file_exist(db_file, path):
    """
    Check if path exists in the database.

    Args:
        db_file (str): Path to the SQLite database file.
        path (str): File path to check in the database.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    query = "SELECT * FROM hashes WHERE path=?"
    result = execute_query(db_file, query, (path,))
    return bool(result)


def get_hashes(db_file):
    """
    Get list of files in the database.
    """
    query = "SELECT * FROM hashes"
    return execute_query(db_file, query)


def add_hash(db_file, path, generated_hash):
    """
    Add hash to the database.
    """
    query = "INSERT INTO hashes VALUES (?, ?)"
    execute_query(db_file, query, (path, generated_hash))


def create_new_database(db_file):
    """
    Create a new database.
    """
    query = (
        "CREATE TABLE IF NOT EXISTS hashes "
        "(path TEXT PRIMARY KEY, hash TEXT)"
    )
    execute_query(db_file, query)

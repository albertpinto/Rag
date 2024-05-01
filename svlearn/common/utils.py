
import os
from pathlib import Path

from .svexception import UnspecifiedDirectoryError, UnspecifiedFileError


# -----------------------------------------------------------------------------
def directory_exists(dir_name: str = None) -> bool:
    """
    Checks if a given directory exists in the filesystem
    :param dir_name: name of the directory as a string
    :return: True if the directory exists, False otherwise.
    """
    if not dir_name:
        raise UnspecifiedDirectoryError('dir_name')
    path = Path(dir_name)
    return path.exists() and path.is_dir()


# -----------------------------------------------------------------------------
def directory_readable(dir_name: str = None) -> bool:
    """
    Checks if a given directory exists and its contents are readable.
    :param dir_name: name of the directory as a string
    :return: True if the directory exists and its contents are readable, False otherwise.
    """
    if not dir_name:
        raise UnspecifiedDirectoryError('dir_name')
    path: Path = Path(dir_name)
    return path.exists() and path.is_dir() and os.access(path, os.R_OK)


# -----------------------------------------------------------------------------
def directory_writable(dir_name: str = None) -> bool:
    """
    Checks if a given directory exists and writable into
    :param dir_name: name of the directory as a string
    :return: True if the directory exists and is writable, False otherwise.
    """
    if not dir_name:
        raise UnspecifiedDirectoryError('dir_name')
    path: Path = Path(dir_name)
    return path.exists() and os.access(path, os.W_OK)


# -----------------------------------------------------------------------------
def directory_is_empty(dir_name: str = None) -> bool:
    """
    Checks if a given directory exists and its contents are readable.
    :param dir_name: name of the directory as a string
    :return: True if the directory exists and is empty, False otherwise.
    """
    if not dir_name:
        raise UnspecifiedDirectoryError('dir_name')
    path: Path = Path(dir_name)
    return path.exists() and path.is_dir() and not path.iterdir()


# -----------------------------------------------------------------------------
def ensure_directory(dir_name: str = None) -> None:
    """
    Checks if a given directory exists and its contents are readable.
    :param dir_name: name of the directory as a string
    :return: True if the directory exists and is empty, False otherwise.
    """
    if not dir_name:
        raise UnspecifiedDirectoryError('dir_name')
    path: Path = Path(dir_name)
    path.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
def file_exists(file_name: str) -> bool:
    """
    Checks if a given file exists in the filesystem
    :param file_name: name of the file as a string
    :return: True if the file exists, False otherwise.
    """
    if not file_name:
        raise UnspecifiedFileError('file_name')
    path = Path(file_name)
    return path.exists() and path.is_file()


def delete_file(file_name: str) -> None:
    """
     Checks if a given file exists in the filesystem, and delete
     it if it does.

     :param file_name: name of the file as a string
     """
    if not file_name:
        raise UnspecifiedFileError('file_name')
    Path(file_name).unlink(missing_ok=True)


def file_is_empty(file_name: str = None) -> bool:
    """
    Checks if a given file exists in the filesystem
    :param file_name: name of the file as a string
    :return: True if the file exists and is empty, False otherwise.
    """
    if not file_name:
        raise UnspecifiedFileError('file_name')
    path = Path(file_name)
    # there seems to be no way yet to directly use pathlib
    return path.exists() and path.is_file() and os.stat(file_name).st_size == 0


def file_not_empty(file_name: str = None) -> bool:
    """
    Checks if a given file exists in the filesystem
    :param file_name: name of the file as a string
    :return: True if the file exists and is not empty, False otherwise.
    """
    return not file_is_empty(file_name)


# -----------------------------------------------------------------------------
def file_readable(file_name: str = None) -> bool:
    """
    Checks if a given file exists and its contents are readable.
    :param file_name: name of the file as a string
    :return: True if the file exists and its contents are readable, False otherwise.
    """
    if not file_name:
        raise UnspecifiedFileError('file_name')
    path: Path = Path(file_name)
    return path.exists() and path.is_file() and os.access(path, os.R_OK)


# -----------------------------------------------------------------------------
def file_writable(file_name: str = None) -> bool:
    """
    Checks if a given file exists and its contents are readable.
    :param file_name: name of the file as a string
    :return: True if the file exists and is writable, False otherwise.
    """
    if not file_name:
        raise UnspecifiedFileError('file_name')
    path: Path = Path(file_name)
    return path.exists() and path.is_file() and os.access(path, os.W_OK)

# -----------------------------------------------------------------------------

def check_valid_file (path:str) -> None:
    """
    Checks if the given path points to an existing, readable, non-empty file
    :param path: the path to the file
    :return: None
    """
  
    if not file_exists(path):
        errorMsg = f'Path does not point to an existing file: {path}'
        raise FileNotFoundError(errorMsg)
    if not file_readable(path):
        errorMsg = f'Path does not point to a readable file: {path}'
        raise FileNotFoundError(errorMsg)
    if  file_is_empty(path):
        errorMsg = f'Path does not point to an empty file: {path}'
        raise FileNotFoundError(errorMsg)  



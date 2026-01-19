# file_io.py
import os
import base64


def encode_file(path):
    """Encode a file as a base64 string.

    Args:
        path: Path to the file to encode.

    Returns:
        Base64-encoded string of the file contents.
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def list_files(dirpath):
    """List files in a directory.

    Args:
        dirpath: Path to the directory containing files.

    Yields:
        Tuples of (filename, filepath).
    """
    for name in os.listdir(dirpath):
        path = os.path.join(dirpath, name)
        if os.path.isfile(path):
            yield name, path

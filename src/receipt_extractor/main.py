# main.py
import json
import argparse

from receipt_extractor import file_io as io_mod
from receipt_extractor import gpt


def process_directory(dirpath):
    """Process all receipt images in a directory.

    Args:
        dirpath: Path to a directory containing receipt image files.

    Returns:
        Dictionary mapping filenames to extracted receipt information.
    """
    results = {}
    for name, path in io_mod.list_files(dirpath):
        image_b64 = io_mod.encode_file(path)
        data = gpt.extract_receipt_info(image_b64)
        results[name] = data
    return results


def main():
    """Command-line entry point for the receipt extractor."""
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args()

    data = process_directory(args.dirpath)
    if args.print:
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()



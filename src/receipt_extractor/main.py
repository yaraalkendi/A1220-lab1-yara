# main.py
import json
import argparse

from receipt_extractor import file_io as io_mod
from receipt_extractor import gpt


def sanitize_amount(value):
    """Sanitize and convert an amount value to float.

    Args:
        value: Amount value as string (may include currency symbol).

    Returns:
        Float amount, or None if conversion fails.
    """
    if value is None:
        return None

    if isinstance(value, str):
        value = value.replace("$", "").strip()

    try:
        return float(value)
    except ValueError:
        return None


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

        # Sanity check: normalize amount
        if isinstance(data, dict) and "amount" in data:
            data["amount"] = sanitize_amount(data["amount"])

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



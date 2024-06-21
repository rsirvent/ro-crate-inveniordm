"""
    This script deposits a RO-Crate directory to an InvenioRDM repository.

    :author: Philipp Beer
    :author: Milan Szente
"""

import argparse
import glob
import json
import os
import sys

import mapping.converter as converter
import upload.uploader as uploader


def main():
    """
    CLI entrypoint. Passes CLI arguments to deposit().
    """

    parser = argparse.ArgumentParser(
        description="Takes a RO-Crate directory as input and uploads it to an InvenioRDM repository"
    )

    parser.add_argument(
        "ro_crate_directory",
        help="RO-Crate directory to upload.",
        type=str,
        action="store",
    )
    parser.add_argument(
        "-d",
        "--datacite",
        help="Optional DataCite metadata file. Skips the conversion process.",
        type=str,
        action="store",
        nargs=1,
    )
    parser.add_argument(
        "-p",
        "--publish",
        help="Publish the record after uploading.",
        action="store_true",
    )
    args = parser.parse_args()

    crate_dir = args.ro_crate_directory
    datacite_list = args.datacite
    publish = args.publish

    datacite_file = datacite_list[0] if datacite_list else None

    deposit(ro_crate_dir=crate_dir, publish=publish, datacite_file=datacite_file)


def deposit(
    ro_crate_dir: str,
    publish: bool = False,
    datacite_file: str | None = None,
):
    """
    The main function of the script.
    It takes a RO-Crate directory as input and uploads it to an InvenioRDM repository.
    """

    # Get all files in RO-Crate directory and check if it is a RO-Crate directory
    # Exclude RO-Crate metadata, and RO-Crate website files
    all_files = []

    for file in glob.glob(f"{ro_crate_dir}/**", recursive=True):
        if "ro-crate-preview" in file or "ro-crate-metadata.json" in file:
            continue
        if os.path.isfile(file):
            all_files.append(file)

    ro_crates_metadata_file = os.path.join(ro_crate_dir, "ro-crate-metadata.json")

    if not os.path.isfile(ro_crates_metadata_file):
        print(
            f"'{ro_crate_dir}' is not a RO-Crate directory: 'ro-crate-metadata.json' not found."
        )
        sys.exit()

    if datacite_file:
        # skip conversion and use the provided file
        with open(datacite_file, "r") as f:
            data_cite_metadata = json.load(f)
    else:
        # convert the RO-Crate metadata to DataCite
        with open(ro_crates_metadata_file, "r") as f:
            ro_crate_metadata = json.load(f)

        metadata_only = False
        if len(all_files) == 0:
            metadata_only = True

        # Convert Metadata
        data_cite_metadata = converter.convert(
            ro_crate_metadata, metadata_only=metadata_only
        )
        # store datacite metadata
        with open("datacite-out.json", "w") as f:
            json.dump(data_cite_metadata, f, indent=4)

    # Upload files
    record_id = uploader.deposit(data_cite_metadata, all_files, publish=publish)

    print(f"Successfully created record {record_id}")
    return record_id


if __name__ == "__main__":
    main()

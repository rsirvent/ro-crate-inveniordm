import json
import os
import re
import shutil
import subprocess

import pytest
import requests

import credentials

CRATES = ["minimal-ro-crate", "test-ro-crate", "real-world-example"]
TEST_DATA_FOLDER = "test/data"
TEST_OUTPUT_FOLDER = "test/output"


@pytest.mark.parametrize("crate_name", [*CRATES])
def test_created_datacite_files(crate_name):
    crate_path = os.path.join(TEST_DATA_FOLDER, crate_name)
    compare_path = os.path.join(TEST_DATA_FOLDER, f"datacite-out-{crate_name}.json")
    with open(compare_path) as expected:
        expected_json = json.load(expected)

    # note - check_output raises CalledProcessError if exit code is non-zero
    log = subprocess.check_output(
        f"python deposit.py {crate_path}", shell=True, text=True
    )
    output_file = "datacite-out.json"
    shutil.copyfile(
        output_file, os.path.join(TEST_OUTPUT_FOLDER, f"datacite-out-{crate_name}.json")
    )
    with open(
        os.path.join(TEST_OUTPUT_FOLDER, f"log-datacite-{crate_name}.txt"),
        "w",
    ) as log_file:
        log_file.write(log)

    assert os.path.exists(output_file)
    with open(output_file) as output:
        output_json = json.load(output)
        assert output_json == expected_json


@pytest.mark.parametrize("crate_name", [*CRATES])
def test_created_invenio_records(crate_name):
    crate_path = os.path.join(TEST_DATA_FOLDER, crate_name)
    compare_path = os.path.join(TEST_DATA_FOLDER, f"datacite-out-{crate_name}.json")
    with open(compare_path) as expected:
        expected_json = json.load(expected)
        expected_metadata = expected_json["metadata"]

    # note - check_output raises CalledProcessError if exit code is non-zero
    log = subprocess.check_output(
        f"python deposit.py {crate_path}", shell=True, text=True
    )
    with open(
        os.path.join(TEST_OUTPUT_FOLDER, f"log-upload-{crate_name}.txt"),
        "w",
    ) as log_file:
        log_file.write(log)
    match = re.search(
        r"^Successfully created record (?P<id>[0-9]*)$", log, flags=re.MULTILINE
    )
    record_id = match.group("id")

    # get the record
    api_url = credentials.repository_base_url
    api_key = credentials.api_key
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {credentials.api_key}",
    }
    record = requests.get(
        f"{api_url}/api/deposit/depositions/{record_id}",
        headers=headers,
    ).json()
    metadata = record["metadata"]

    assert metadata["title"] == expected_metadata["title"]
    assert metadata["upload_type"] == expected_metadata["resource_type"]["id"]
    assert metadata["access_right"] == "open"
    assert len(metadata["creators"]) == len(expected_metadata["creators"])
    if "contributors" in expected_metadata:
        assert len(metadata["contributors"]) == len(expected_metadata["contributors"])
    else:
        assert "contributors" not in metadata

    if expected_json["files"]["enabled"]:
        assert len(record["files"]) != 0
        for file in record["files"]:
            filename = file["filename"]
            with open(
                os.path.join(TEST_DATA_FOLDER, crate_name, filename)
            ) as local_file:
                remote_file_data = requests.get(
                    file["links"]["download"], headers=headers
                ).content
                assert local_file.read() == remote_file_data.decode()
    else:
        assert len(record["files"]) == 0
    assert record["state"] == "unsubmitted"
    assert record["submitted"] == False

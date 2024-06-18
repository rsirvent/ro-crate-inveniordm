import os
import subprocess
import shutil
import json
import pytest

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
        os.path.join(TEST_OUTPUT_FOLDER, f"log-{crate_name}.txt"),
        "w",
    ) as log_file:
        log_file.write(log)

    assert os.path.exists(output_file)
    with open(output_file) as output:
        output_json = json.load(output)
        assert output_json == expected_json

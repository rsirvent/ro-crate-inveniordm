import os
from unittest import mock

import rocrate_inveniordm.upload.uploader as uploader


@mock.patch.dict(os.environ, {"INVENIORDM_API_KEY": "test-key"})
def test_get_headers():
    input = "application/json"
    expected = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer test-key",
    }

    result = uploader.get_headers(input)

    assert result == expected

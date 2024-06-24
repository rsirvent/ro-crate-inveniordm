import os
import pytest
from unittest import mock

import upload.credentials as credentials


@mock.patch.dict(os.environ, {"INVENIORDM_API_KEY": ""})
def test_get_api_key__not_set():

    with pytest.raises(ValueError):
        credentials.get_api_key()


@mock.patch.dict(os.environ, {"INVENIORDM_API_KEY": "example-for-testing"})
def test_get_api_key__set():

    key = credentials.get_api_key()

    assert key == "example-for-testing"


@mock.patch.dict(os.environ, {"INVENIORDM_BASE_URL": ""})
def test_get_repository_base_url__not_set():

    with pytest.raises(ValueError):
        credentials.get_repository_base_url()


@mock.patch.dict(os.environ, {"INVENIORDM_BASE_URL": "https://example.org"})
def test_get_repository_base_url__set():

    key = credentials.get_repository_base_url()

    assert key == "https://example.org"

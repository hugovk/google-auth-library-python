# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import os
import pytest

from google.auth import api_key
from google.auth import environment_vars


def test_credentials_constructor():
    with pytest.raises(ValueError) as excinfo:
        api_key.Credentials("")

    assert excinfo.match(r"Token must be a non-empty API key string")


def test_expired_and_valid():
    credentials = api_key.Credentials("api-key")

    assert credentials.valid
    assert credentials.token == "api-key"
    assert not credentials.expired

    credentials.refresh(None)
    assert credentials.valid
    assert credentials.token == "api-key"
    assert not credentials.expired


def test_before_request():
    credentials = api_key.Credentials("api-key")
    headers = {}

    credentials.before_request(None, "http://example.com", "GET", headers)
    assert headers["x-goog-api-key"] == "api-key"


def test_get_api_key_credentials_no_api_key():
    cred = api_key.get_api_key_credentials("api-key")
    assert isinstance(cred, api_key.Credentials)
    assert cred.token == "api-key"


def test_get_api_key_credentials():
    cred = api_key.get_api_key_credentials("api-key")
    assert isinstance(cred, api_key.Credentials)
    assert cred.token == "api-key"


def test_get_api_key_credentials_from_env_var():
    with mock.patch.dict(os.environ, {environment_vars.API_KEY: "api-key"}):
        cred = api_key.get_api_key_credentials()
        assert isinstance(cred, api_key.Credentials)
        assert cred.token == "api-key"

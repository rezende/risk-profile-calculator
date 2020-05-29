#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon
from falcon import testing
import json
import pytest
from unittest.mock import mock_open, call

from risk_api.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)


# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_list_images(client):
    doc = {
        'a': 'b'
    }

    response = client.simulate_get('/calculator')
    print("===============")
    print(response.content)
    result_doc = json.loads(response.content)

    assert result_doc == doc
    assert response.status == falcon.HTTP_OK


# "monkeypatch" is a special built-in pytest fixture that can be
# used to install mocks.
def test_posted_image_gets_saved(client, monkeypatch):
    mock_file_open = mock_open()
    monkeypatch.setattr('io.open', mock_file_open)

    fake_uuid = '123e4567-e89b-12d3-a456-426655440000'
    monkeypatch.setattr('uuid.uuid4', lambda: fake_uuid)

    # When the service receives an image through POST...
    fake_image_bytes = b'fake-image-bytes'
    response = client.simulate_post(
        '/calculator',
        body=fake_image_bytes,
        headers={'content-type': 'image/png'}
    )

    # ...it must return a 201 code, save the file, and return the
    # image's resource location.
    assert response.status == falcon.HTTP_CREATED
    assert call().write(fake_image_bytes) in mock_file_open.mock_calls
    assert response.headers['location'] == '/calculator/{}.png'.format(fake_uuid)

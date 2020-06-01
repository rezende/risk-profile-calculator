#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon
from falcon import testing
import json
import pytest

from risk_api.app import api
from risk_api.constants import Constants as c


@pytest.fixture
def client():
    return testing.TestClient(api)

@pytest.fixture
def base_data():
    return {
      c.DATA_AGE: 35,
      c.DATA_DEPENDENTS: 2,
      c.DATA_HOUSE: {c.DATA_OWNERSHIP_STATUS: c.OWNED},
      c.DATA_INCOME: 100000,
      c.DATA_MARITAL_STATUS: c.MARRIED,
      c.DATA_RISK_QUESTIONS: [0, 1, 0],
      c.DATA_VEHICLE: {c.DATA_V_YEAR: 2011}
    }


def test_post(client, base_data):
    response = client.simulate_post(
        '/calculator',
        body=json.dumps(base_data),
        headers={'content-type': 'application/json'}
    )
    assert response.json[c.INS_AUTO] == 'economic'
    assert response.json[c.INS_DISABILITY] == 'economic'
    assert response.json[c.INS_HOME] == 'economic'
    assert response.json[c.INS_LIFE] == 'regular'
    assert response.status == falcon.HTTP_OK

def test_missing_field(client, base_data):
    del base_data[c.DATA_AGE]
    response = client.simulate_post(
        '/calculator',
        body=json.dumps(base_data),
        headers={'content-type': 'application/json'}
    )
    assert response.status == falcon.HTTP_BAD_REQUEST
    content = json.loads(response.content)
    assert content['title'] == 'Request data failed validation'
    assert content['description'] == "'age' is a required property"

def test_wrong_string_option(client, base_data):
    base_data[c.DATA_MARITAL_STATUS] = 'widow'
    response = client.simulate_post(
        '/calculator',
        body=json.dumps(base_data),
        headers={'content-type': 'application/json'}
    )
    #  __import__('pudb').set_trace()
    assert response.status == falcon.HTTP_BAD_REQUEST
    content = json.loads(response.content)
    assert content['title'] == 'Request data failed validation'
    assert content['description'] == "'widow' does not match '^single|married$'"

def test_negative_number(client, base_data):
    base_data[c.DATA_AGE] = -7
    response = client.simulate_post(
        '/calculator',
        body=json.dumps(base_data),
        headers={'content-type': 'application/json'}
    )
    assert response.status == falcon.HTTP_BAD_REQUEST
    content = json.loads(response.content)
    assert content['title'] == 'Request data failed validation'
    assert content['description'] == '-7 is less than the minimum of 0'

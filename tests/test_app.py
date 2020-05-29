#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon
from falcon import testing
import json
import pytest
from unittest.mock import mock_open, call

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
      c.DATA_HOUSE: {c.DATA_OWNERSHIP_STATUS: c.DATA_OS_OWNED},
      c.DATA_INCOME: 0,
      c.DATA_MARITAL_STATUS: c.DATA_MS_MARRIED,
      c.DATA_RISK_QUESTIONS: [0, 1, 0],
      c.DATA_VEHICLE: {c.DATA_V_YEAR: 2018}
    }


def test_inelegible_for_auto(client, base_data):
    base_data[c.DATA_VEHICLE] = {}
    response = client.simulate_post(
        '/calculator',
        body=json.dumps(base_data),
        headers={'content-type': 'application/json'}
    )
    assert response.json[c.INS_AUTO] == c.PLAN_INELEGIBLE
    assert response.status == falcon.HTTP_OK

def test_inelegible_for_disability_by_income(client, base_data):
    base_data[c.DATA_INCOME] = 0
    response = client.simulate_post(
        '/calculator',
        body=json.dumps(base_data),
        headers={'content-type': 'application/json'}
    )
    assert response.json[c.INS_DISABILITY] == c.PLAN_INELEGIBLE
    assert response.status == falcon.HTTP_OK

def test_inelegible_for_disability_by_age(client, base_data):
    base_data[c.DATA_AGE] = 88
    response = client.simulate_post(
        '/calculator',
        body=json.dumps(base_data),
        headers={'content-type': 'application/json'}
    )
    assert response.json[c.INS_DISABILITY] == c.PLAN_INELEGIBLE
    assert response.status == falcon.HTTP_OK

def test_inelegible_for_house(client, base_data):
    base_data[c.DATA_HOUSE] = {}
    response = client.simulate_post(
        '/calculator',
        body=json.dumps(base_data),
        headers={'content-type': 'application/json'}
    )
    assert response.json[c.INS_HOME] == c.PLAN_INELEGIBLE
    assert response.status == falcon.HTTP_OK

def test_default_score(client, base_data):
    pass

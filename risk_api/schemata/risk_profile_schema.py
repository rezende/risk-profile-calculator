#!/usr/bin/env python
# -*- coding: utf-8 -*-

from risk_api.constants import Constants as c

request_schema = {
    "type" : "object",
    "properties" : {
        c.DATA_AGE: {"type" : "integer", "minimum": 0},
        c.DATA_DEPENDENTS: {"type": "integer", "minimum": 0},
        c.DATA_HOUSE: {
            "type": "object",
            "properties": {
                c.DATA_OWNERSHIP_STATUS: {
                    "type": "string",
                    "pattern": "^owned|mortgaged$"
                }
            },
            "required": [c.DATA_OWNERSHIP_STATUS]
        },
        c.DATA_INCOME: {"type": "integer", "minimum": 0},
        c.DATA_MARITAL_STATUS: {
            "type": "string",
            "pattern": "^single|married$"
        },
        c.DATA_RISK_QUESTIONS: {
            "type": "array",
            "items": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1,
                "minItems": 3,
                "maxItems": 3
            }
        },
        c.DATA_VEHICLE: {
            "type" : "object",
            "properties": {
                c.DATA_V_YEAR: {
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": [c.DATA_V_YEAR]
        },
    },
    "required": [c for c in c.REQUIRED_FIELDS]
}

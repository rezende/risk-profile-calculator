#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon

from .calculator import Calculator

api = application = falcon.API()

calculator = Calculator(storage_path='.')
api.add_route('/calculator', calculator)

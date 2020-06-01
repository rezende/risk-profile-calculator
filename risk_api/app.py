#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon

from risk_api.resources import RiskProfileResource

api = application = falcon.API()

api.add_route('/calculator', RiskProfileResource())

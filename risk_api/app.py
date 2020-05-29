#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon

from .risk_profile_resource import RiskProfileResource

api = application = falcon.API()

api.add_route('/calculator', RiskProfileResource())

import json
from falcon.media.validators import jsonschema
from risk_api.schemata.risk_profile_schema import request_schema
from risk_api.operations import RiskProfileOperation


class RiskProfileResource:
    @jsonschema.validate(request_schema)
    def on_post(self, req, resp):
        resp.body = json.dumps(
            RiskProfileOperation(req.media).run()
        )

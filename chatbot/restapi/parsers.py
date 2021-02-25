from flask_restplus import fields
from collections import OrderedDict

from restapi.restplusapi import api

predict_user_input_json = api.model('predict_user_input_json', OrderedDict([
    ('user_desc', fields.String(required=True, description='Description of the user', attribute='user_desc', example="Unable to access the service")),
    ('user_id', fields.String(required=True, description='ID of the user', attribute='user_id', example="user1")),
    ('agent_status', fields.String(required=True, description='Agent interaction status (y/n)', attribute='user_id', example="y"))
]))

predict_user_request_header = api.model('predict_user_request_header', {
    'Authorization': fields.String(required=True, description='Access Token', example="Bearer Axin2903-2344dsfl"),
})

predict_user_output_json = api.model('predict_user_output_json', {
    ('user_desc', fields.String(required=True, description='Description of the user', attribute='user_desc', example="Unable to access the service")),
    ('user_id', fields.String(required=True, description='ID of the user', attribute='user_id', example="user1"))
})

not_found_error = api.inherit('not_found_error', {
    'title': fields.String(description='Resource Not Found', required=True, example="No Data Found"),
    'detail': fields.String(description='Requested resource was not found', required=True,
                            example="working_no / season Not Found"),
    'status': fields.String(description='HTTP Status code', required=True, example="404")
})

bad_request = api.inherit('bad_request', {
    'title': fields.String(description='Bad Request', required=True, example="Bad Request"),
    'detail': fields.String(description='Validation of Input parameters failed', required=True,
                            example="Validation of the Input parameters failed"),
    'status': fields.String(description='HTTP Status code', required=True, example="400"),
})

internal_server_error = api.inherit('internal_server_error', {
    'title': fields.String(description='Internal Server Error', required=True, example="Internal Server Error"),
    'detail': fields.String(description='Request could not be processed due to Internal Server Error', required=True,
                            example="Prediction failed due to Internal Server Error"),
    'status': fields.String(description='HTTP Status code', required=True, example="500")
})
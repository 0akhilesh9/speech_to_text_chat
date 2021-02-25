import re
import sys
import copy
import json
import datetime
import requests
import traceback
from flask_restplus import abort
from flask_restplus import Resource
from werkzeug.exceptions import HTTPException
from flask import request, jsonify, make_response

import prediction.utility as utility
from restapi.restplusapi import api
from restapi.ChatbotException import ChatbotException
from restapi.parsers import bad_request, not_found_error, internal_server_error
from restapi.parsers import predict_user_input_json, predict_user_output_json, predict_user_request_header


ns = api.namespace('chatagent', description='Return response')
#parser = ns.parser()
#parser.add_argument('Authorization', type=str,location='headers',help='Bearer Access Token', required=False)

@ns.route('/')
#@api.expect(parser, validate=False)
class Prediction(Resource):
    
    #@api.expect(predict_user_input_json, name='predict_user_input_json', validate=False)
    #@api.response(200, 'Success', predict_user_output_json)
    #@api.response(500, 'Internal Server Error', internal_server_error)
    #@api.response(404, 'Resource Not Found', not_found_error)
    #@api.response(400, 'Bad Request', bad_request)
    
    def post(self):
        """
        Returns the response for the input json.
        """
        rest_response = {}
        status = 200

        try:            
            rest_input = json.loads(request.data)
            
            print("Chatbot input:")
            print(rest_input)
            rest_response = {'chatbot_text': 'This is msg from chatbot'}
            resp = make_response(jsonify(rest_response), status)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except (Exception) as error:
            print("########################################")
            print("##### Error servicing prediction request!!!")
            print("########################################")
            traceback.print_exc()
            raise ChatbotException(detail='Prediction service failed due to internal server error!', status=500)    
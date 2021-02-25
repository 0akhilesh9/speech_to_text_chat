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
from restapi.ChatException import ChatException
from restapi.parsers import bad_request, not_found_error, internal_server_error
from restapi.parsers import predict_user_input_json, predict_user_output_json, predict_user_request_header


ns = api.namespace('agent', description='Connect to agent')

chat_obj = {"context":"","in_msg":[],"out_msg":[],"resp":"","init":False,"req":""}
@ns.route('/')
class Prediction(Resource):
  
    @api.response(200, 'Success', predict_user_output_json)
    @api.response(500, 'Internal Server Error', internal_server_error)
    @api.response(404, 'Resource Not Found', not_found_error)
    @api.response(400, 'Bad Request', bad_request)
    
    def post(self):
        rest_response = {}
        status = 200
        
        try:            
            rest_input = json.loads(request.data)
            if(chat_obj['init']):
                if 'poll' not in rest_input.keys():
                    chat_obj['resp']=rest_input['user_desc']
                rest_response = {'user_response': chat_obj['req'], 'context':chat_obj['context']}
                resp = make_response(jsonify(rest_response), status)
                resp.headers['Access-Control-Allow-Origin'] = '*'
                resp.headers['Access-Control-Allow-Credentials']= 'true'
                resp.headers['Access-Control-Allow-Methods']= 'POST'
                resp.headers['Access-Control-Allow-Headers']= 'Content-Type'
                chat_obj['req'] = ""
                return resp       
            else:
                rest_response = {'user_response': chat_obj['req'], 'context':chat_obj['context']}
                resp = make_response(jsonify(rest_response), status)
                resp.headers['Access-Control-Allow-Origin'] = '*'
                resp.headers['Access-Control-Allow-Credentials']= 'true'
                resp.headers['Access-Control-Allow-Methods']= 'POST'
                resp.headers['Access-Control-Allow-Headers']= 'Content-Type'
                return resp   
            
        except (ChatException, HTTPException) as error:
            data = getattr(error, 'data', str(error))
            
            ####For raised custom exceptions
            if isinstance(error, ChatException):
                raise
            ####For parameter validation failures
            elif isinstance(error, HTTPException) and getattr(error, 'code', 500) == 400 and isinstance(data,dict):
                raise
            else:
                print("########################################")
                print("##### Error servicing prediction request!!!")
                print("########################################")
                traceback.print_exc()
                raise ChatException(detail='Prediction service failed due to internal server error!', status=500)

        except (Exception) as error:
            print("########################################")
            print("##### Error servicing prediction request!!!")
            print("########################################")
            traceback.print_exc()
            raise ChatException(detail='Prediction service failed due to internal server error!', status=500)    
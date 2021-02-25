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
from restapi.agent import chat_obj
from restapi.ChatException import ChatException
from restapi.parsers import bad_request, not_found_error, internal_server_error
from restapi.parsers import predict_user_input_json, predict_user_output_json, predict_user_request_header


ns = api.namespace('predict_user', description='Return predicted suggestions for input')
parser = ns.parser()
parser.add_argument('Authorization', type=str,location='headers',help='Bearer Access Token', required=False)

user_obj = {"in_msg":[],"bot_msg":[],"agent_msg":[],"transac":[]}

@ns.route('/')
@api.expect(parser, validate=False)
class Prediction(Resource):
        
    
    @api.expect(predict_user_input_json, name='predict_user_input_json', validate=False)
    @api.response(200, 'Success', predict_user_output_json)
    @api.response(500, 'Internal Server Error', internal_server_error)
    @api.response(404, 'Resource Not Found', not_found_error)
    @api.response(400, 'Bad Request', bad_request)
    
    def post(self):
        """
        Returns the predicted suggestions for the input json.
        """
        rest_response = {}
        status = 200
        user_name = 'A user'
        user_email = 'user@email.com'
        
        try:            
            rest_input = json.loads(request.data)
            errors = {}
            print(rest_input)
            #for i in range(0,100000): pass
            ####Input validation
            # for key in rest_input:
                # rest_input[key] = rest_input[key].strip()
                # if rest_input[key] == "" or not rest_input[key]:
                    # errors[key] = "Invalid value for field '" + key + "'. Example: " + predict_user_input_json[key].example + "."               
            # if errors:
                # print("##### Input parameter validation failed")
                # abort(400, message='Bad request. Validation of the Input parameters failed!!!', errors=errors) 
            
            if 'clean' in rest_input.keys():
                for key in chat_obj.keys():
                    chat_obj[key] = []
                chat_obj['context']=""
                chat_obj['init']=False
                chat_obj['resp']=""
                chat_obj['req']=""
                for key in user_obj.keys():
                    user_obj[key]=[]
                            
            if 'poll' not in rest_input.keys():
                user_obj['in_msg'].append(rest_input['user_desc'])
                user_obj['transac'].append("User: " + str(rest_input['user_desc']))
            
            if rest_input['agent_status'] == 'n': 
                        
                ####To commnicate with chatbot
                req1_url = utility.config_data['chatbotURL']
                req1_payload = {}
                for key in rest_input.keys():
                    req1_payload[key] = rest_input[key]
                headers = {"content-type": "application/json", "Accept": "application/json"}#, "Authorization": "Bearer " + 'access_token'}
                req1_response = requests.post(req1_url, data=json.dumps(req1_payload), headers=headers)
                
                if req1_response.status_code != requests.codes.ok:
                    req1_response.raise_for_status()    
                rest_response["user_response"] = str(req1_response.json()['chatbot_text'])
                user_obj['bot_msg'].append(str(req1_response.json()['chatbot_text']))
                user_obj['transac'].append("Bot: " + str(req1_response.json()['chatbot_text']))
                
                resp = make_response(jsonify(rest_response), status)
                resp.headers['Access-Control-Allow-Origin'] = '*'
                resp.headers['Access-Control-Allow-Credentials']= 'true'
                resp.headers['Access-Control-Allow-Methods']= 'POST'
                resp.headers['Access-Control-Allow-Headers']= 'Content-Type'
                return resp             
            
            else:            
            ####To chatagent                
                                
                if 'poll' not in rest_input.keys():
                    chat_obj['req'] = rest_input['user_desc']
                req2_payload = {}
                if(not chat_obj['init']):
                    chat_obj['init']=True
                    chat_obj['context'] = user_obj['transac']
                    rest_response["user_response"] = "Please wait for the agent to reply."
                    resp = make_response(jsonify(rest_response), status)
                    resp.headers['Access-Control-Allow-Origin'] = '*'
                    resp.headers['Access-Control-Allow-Credentials']= 'true'
                    resp.headers['Access-Control-Allow-Methods']= 'POST'
                    resp.headers['Access-Control-Allow-Headers']= 'Content-Type'
                    print("##########################")
                    print(rest_response)
                    print("##########################")
                    return resp                        
                
                rest_response["user_response"] = chat_obj['resp']
                chat_obj['resp'] = ""
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
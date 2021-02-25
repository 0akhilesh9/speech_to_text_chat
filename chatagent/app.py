import os
import sys
import yaml
import traceback
from flask_cors import CORS, cross_origin
from flask import Blueprint, Flask, json, jsonify, render_template

import prediction.utility as utility
from restapi.restplusapi import api
from restapi.user import ns as user

app = Flask(__name__)
cors = CORS(app)

def initialize_prediction_module():
    utility.load_config()

def initialize_flask(flask_app):    
    blueprint = Blueprint('api', __name__, url_prefix='/user-api')
    api.init_app(blueprint)
    api.add_namespace(user)
    flask_app.register_blueprint(blueprint)    

def main(webservice_flag):
    try:
        print("\n<**************************************************>\n")    
        initialize_prediction_module()

        initialize_flask(app)
        app.run(host=utility.config_data['flaskData']['host'], port=utility.config_data['flaskData']['port'], threaded=True, debug=utility.config_data['flaskData']['debugFlag'],ssl_context=('resources/certificate.cert','resources/pkey.key' ))       

        print("\n<**************************************************>\n")
    except (Exception) as error:
        traceback.print_exc(file=sys.stdout)

@app.route('/user')
def user_endpoint():
    title = 'Create the input'
    return render_template('user.html', title=title)        

@app.route('/agentui')
def agent_endpoint():
    title = 'Create the input'
    return render_template('agent.html', title=title)        
        
                           
if __name__ == '__main__':
    main(True)
import sys
import yaml
import traceback
from flask_cors import CORS, cross_origin
from flask import Blueprint, Flask, json, jsonify

import prediction.utility as utility
from restapi.restplusapi import api
from restapi.chatbot import ns as chatbot


app = Flask(__name__)
cors = CORS(app)

def initialize_prediction_module():
    utility.load_config()
    
def initialize_flask(flask_app):    
    blueprint = Blueprint('api', __name__, url_prefix='/chatbot-prediction')
    api.init_app(blueprint)
    api.add_namespace(chatbot)
    flask_app.register_blueprint(blueprint)    

def main(webservice_flag):
    try:
        print("\n<**************************************************>\n")    
        initialize_prediction_module()

        initialize_flask(app)
        app.run(host=utility.config_data['flaskData']['host'], port=utility.config_data['flaskData']['port'], threaded=True, debug=utility.config_data['flaskData']['debugFlag'])       

        print("\n<**************************************************>\n")
    except (Exception) as error:
        traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
    main(True)
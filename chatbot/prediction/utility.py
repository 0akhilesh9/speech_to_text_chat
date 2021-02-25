import os
import sys
import yaml
import traceback

config_data = None

def load_config():
    global config_data
    config_file_path = os.path.join('resources', 'config.yaml')
    
    try:
        with open(config_file_path, 'r') as stream:
            config_data = yaml.load(stream)
        print("->Loaded config file successfully.")    
    except:
        print("########################################")
        print("##### Cannot load config file!!!")
        print("########################################")
        traceback.print_exc()
        sys.exit()
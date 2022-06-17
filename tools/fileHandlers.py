import imp
import json 
import os 
import sys 
from colorama import Fore, init
init(autoreset=True)

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

def read_settings_data():
    """
    Reads the connection string from the settings file
    :return:
    """
    print(project_path)
    path = f'{project_path}/systemSettings.json'
    try:
        with open(path) as json_file:
            data = json.load(json_file)
            return data
    except IOError:
        return None


def read_last_checked_block_data():
    """
    Loads the last block height which was stored in last_block.json
    :return: Block height as INT
    """

    # Reads last marked block data in the document

    try:
        with open('lastBlock.json') as json_file:
            data = json.load(json_file)
            last_marked_blocked = data["blockHeight"]
            return int(last_marked_blocked)
    except IOError as e:
        print(Fore.RED + f'{e}')
        data = {"blockHeight": 800000}

        with open('lastBlock.json', 'w') as f:
            json.dump(data, f)
            return int(data['blockHeight'])


def store_last_updated_block_height(block_height):
    """
    Stores the height of last block which was monitored for incoming transactions
    :param block_height: block height from RPC Daemon as INT
    :return: Updates the value in last_block.json
    """
    try:
        data = {"blockHeight": block_height}

        with open('lastBlock.json', 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'[DEP-BLOCK] Json update error: {e}')
        return False
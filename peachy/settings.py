import json
import sys


def get_setting(setting_name):
    try:
        return SETTINGS[setting_name]
    except KeyError:
        raise


def load_settings(settings_filename):
    with open(settings_filename, 'r') as infile:
        settings = json.load(infile)
    return settings


try:
    settings_filename = sys.argv[1]
except IndexError:
    print("please provide the path to a configuration json file")
    sys.exit()

SETTINGS = load_settings(settings_filename)

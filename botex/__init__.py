from telebot import logger
import configparser
import yaml

try :
    with open('messages.yaml', 'r') as f :
        messages = yaml.safe_load(f)
except Exception as e :
    logger.error(f'Could not load messages file:\n{repr(e)}')
    exit(1)

try :
    config = configparser.ConfigParser()
    with open('config.ini') as f :
        config.read_file(f)
except Exception as e :
    logger.error(f'Could not load config file:\n{repr(e)}')
    exit(1)


from pathlib import Path
from credentials import get_credentials, Credential, username_entry, password_entry
import traceback
import sys
import logging
from logging import basicConfig as basic_config

basic_config(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s - [file: %(filename)s]",
    datefmt="%Y-%m-%d %T WAT",
    style="%",
    filename='error.log',
    filemode="a",
    encoding="utf-8"
)

class Error:
    def __init__(self):
        pass

    @staticmethod
    def get_error_details():
      error_type, error_message, error_traceback = sys.exc_info()
      error_name = error_type.__name__
      frames = traceback.extract_tb(error_traceback)
      line_no = next(frame.lineno for frame in reversed(frames) if frame.filename == __file__)
      return error_name, error_message, line_no

    @staticmethod
    def error():
        error_name, error_message, line_no = Error.get_error_details()
        logging.error("%s - %s - [line %s]", error_name, error_message, line_no)

    @staticmethod
    def critical():
        error_name, error_message, line_no = Error.get_error_details()
        logging.critical("%s - %s - [line %s]", error_name, error_message, line_no)

try:
    credentials_dir = Path('credentials.json').expanduser()
    my_credential = get_credentials(credentials_dir)
    credential_file = Credential(my_credential)
    user_name = username_entry()
    pass_word = password_entry()
    credential_file.authenticate(user_name, pass_word)
    print(f"""
        {credential_file.usernames()}
        {credential_file.passwords()}
        {credential_file.usernames_and_passwords()}""" 
    )
except:
    Error.error()

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from operator import truediv, mul
import traceback
import sys
import logging


class Error:
    def __init__(self):
        pass
     
    @staticmethod
    def get_error_details():
        error_type, error_message, error_traceback = sys.exc_info()
        error_name = error_type.__name__
        frames = traceback.extract_tb(error_traceback)
        line_no = next(frame.lineno for frame in reversed(frames) if frame filename == __file__)
        return error_name, error_message, line_no
        
    @staticmethod
    def error():
        error_name, error_message, line_no = Error.get_error_details()   
        print()  
    
def image(value_a, value_b):
    try:
        result = truediv(value_a, value_b)
        next = mul(result, value_b)
        print(f'Output -> {next}')
    except:
        
        
        
    
import pandas as pd
import re
from pathlib import Path


file = Path('amazon.xlsx').expanduser()
data = pd.read_excel(file, sheet_name='in')


def clean_field(field):
    cleaned_field = re.sub(r'[^\d.]', '', field]
    return float(cleaned_field) if cleaned_field else None

if __name__ = '__main__':
    try:
        data['discounted_price'] = data['discounted_price'].apply(clean_field)
    except:
        import sys
        import traceback
        
        error_type, error_message, error_traceback = sys.exc_info()
        error_name = error_type.__name__
        frames = traceback.extract_tb(error_traceback)
        line_no = next((frame.lineno for frame in reversed(frames) if frame.filename == __file__), 'unknown')
        print(f"{error_name} - {error_message} [line {line_no}]")


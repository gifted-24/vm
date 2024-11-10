import pandas as pd
import re
from pathlib import Path


file = Path('amazon.xlsx').expanduser()
data = pd.read_excel(file, sheet_name='in')
def clean_field(field):
    cleaned_field = re.sub(r'[^\d.]', '', field]
    return float(cleaned_field


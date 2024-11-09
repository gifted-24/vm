import pandas as pd
import re
from pathlib import Path


file = Path('amazon.xlsx').expanduser()
data = pd.read_excel(file, sheet_name='in')
print(data)

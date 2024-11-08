import kagglehub
from pathlib import Path
from shutil import move


kaggle = kagglehub
destination = Path('mobile_sales_dataset')
path = kaggle.dataset_download("waqi786/mobile-sales-dataset")
move(path, destination)

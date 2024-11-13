import pandas as pd
import re
from pathlib import Path
import json


file = 'amazon.xlsx'
data = pd.read_excel(file, sheet_name='in')


def filter_num(num):
    filtered_num = re.sub(
        r'[^\d.]', '', 
        str(num)
    )
    return float(filtered_num) if filtered_num else None


def filter_text(text):
    remove_strange_characters_from_text = re.sub(
        r'[^\da-zA-Z.-?,\'\"/]+', ' ', 
        str(text)
    )
    start_text_with_alpha_numeric = re.sub(
        r'^[^A-Za-z\d]+', '', 
        remove_strange_characters_from_text
    )
    text_with_normalized_spaces = re.sub(
        r'\s+', ' ', 
        start_text_with_alpha_numeric
    ).strip()
    return text_with_normalized_spaces if text_with_normalized_spaces else None


def convert_to_sales_metric(value, index): #revenue #capital
    multiplier = len(data['user_id'][index].split(','))
    new_value = (value * multiplier)
    return new_value if new_value else None


try:
    data.rename(columns={
        'discounted_price': 'capital',
        'actual_price': 'revenue',
        'discount_percentage': 'profit_margin',
        'rating': 'product_rating'
        },
        inplace=True
    )
    for field in ['capital', 'revenue', 'profit_margin', 'product_rating']:
        data[field] = data[field].apply(filter_num)
        data[field] = pd.to_numeric(data[field], errors = 'coerce')
        if field in {'capital', 'revenue', 'product_rating'}:
            data[field] = data[field].fillna(0)
            count = len(data[field])
            index = range(0, count)
            data[field] = list(map(
                convert_to_sales_metric, data[field], index
                )
            )
        if field == 'product_rating':
            max_possible_rating = list(map(
                lambda value: convert_to_sales_metric(5, value), index
                )
            )
            data['max_possible_rating'] = max_possible_rating
            data['product_rating'] = data['product_rating'].fillna(
                data['product_rating'].mean()
            )
    for field in ['product_name', 'user_id']:
        data[field] = data[field].apply(filter_text)
    data['category'] = data['category'].apply(
        lambda text: text.strip().split('|')[0] if isinstance(text, str) else
        text.strip().split('|')[1]
    )
    data = data.drop(columns=[
        'img_link', 
        'review_title', 
        'review_id',
        'product_link',
        'about_product',
        'review_content',
        'product_id',
        'Unnamed: 3',
        'user_name',
        'rating_count'
        ]
    )
except:
    import sys
    import traceback        
    error_type, error_message, error_traceback = sys.exc_info()
    error_name = error_type.__name__
    frames = traceback.extract_tb(error_traceback)
    line_no = next(
        frame.lineno for frame in reversed(frames) 
        if frame.filename == __file__
    )
    print(f"{error_name} - {error_message} [line {line_no}]")


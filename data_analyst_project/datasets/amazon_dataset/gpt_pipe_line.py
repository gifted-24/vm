import pandas as pd
import re

# Load the dataset
file_path = '/mnt/data/amazon.xlsx'
data = pd.read_excel(file_path, sheet_name='in')

# Step 1: Cleaning Price Columns
# Convert 'discounted_price' and 'actual_price' to numeric by removing unwanted characters
def clean_price(price):
    # Remove currency symbols and commas, then convert to float
    clean = re.sub(r'[^0-9.]', '', price)
    return float(clean) if clean else None

data['discounted_price'] = data['discounted_price'].apply(clean_price)
data['actual_price'] = data['actual_price'].apply(clean_price)

# Step 2: Convert Discount Percentage to Numeric
data['discount_percentage'] = pd.to_numeric(data['discount_percentage'], errors='coerce')

# Step 3: Parsing Categories
# Extracting primary category from the category hierarchy
data['primary_category'] = data['category'].apply(lambda x: x.split('|')[0] if isinstance(x, str) else None)

# Step 4: Dropping Irrelevant or Redundant Columns
# Remove columns that are not directly useful for the analysis, like user_id, user_name, and review_id
data = data.drop(columns=['user_id', 'user_name', 'review_id'])

# Step 5: Handling Missing Values
# Filling missing numeric fields with zeros and other strategies for categorical fields
data['discounted_price'] = data['discounted_price'].fillna(0)
data['actual_price'] = data['actual_price'].fillna(0)
data['rating'] = data['rating'].fillna(data['rating'].mean())  # Fill missing ratings with average rating

# Step 6: Creating New Features
# Calculate potential profit margin
data['potential_profit'] = data['actual_price'] - data['discounted_price']

# Step 7: Convert Ratings to Numeric
# Ensure ratings are in numeric format to facilitate analysis
data['rating'] = pd.to_numeric(data['rating'], errors='coerce')

# Step 8: Standardize Column Names
# Renaming columns to consistent snake_case naming convention
data.rename(columns={
    'product_id': 'product_id',
    'product_name': 'product_name',
    'category': 'category',
    'discounted_price': 'discounted_price',
    'actual_price': 'actual_price',
    'discount_percentage': 'discount_percentage',
    'rating': 'rating',
    'rating_count': 'rating_count',
    'about_product': 'about_product',
    'img_link': 'img_link',
    'product_link': 'product_link'
}, inplace=True)

# Display the cleaned dataset for verification
import ace_tools as tools
tools.display_dataframe_to_user(name="Cleaned Amazon Dataset", dataframe=data)


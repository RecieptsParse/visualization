import os
import json
import sys
import subprocess

# try:
#     subprocess.run(['/bin/bash', 'install_packages.sh'], check=True)
# except subprocess.CalledProcessError as e:
#     print(f"Error running shell script: {e}")

import streamlit as st
import pandas as pd

with open("data/classified_receipts.json", 'r') as json_file:
    # Load the JSON data
    data = json.load(json_file)

vendor_data = []
for i,entry in enumerate(data):
    entry_data = entry["ReceiptInfo"]
    entry_data['entry_id'] = i
    vendor_data.append(entry_data)


df_vendor_data = pd.DataFrame(vendor_data)

df_vendor_data = df_vendor_data.drop(columns=['ITEMS'])
print(df_vendor_data)

product_data = []

for i, entry in enumerate(data):
    entry_data = entry['ReceiptInfo']['ITEMS']
    for j, items in enumerate(entry_data):
        items['item_id'] = i
        product_data.append(items)
    
df_product_data = pd.DataFrame(product_data)

df_product_data = df_product_data.drop(columns=['includedItems'])


count_product = df_product_data['productClassification'].value_counts()

print(count_product)

count_vendor = df_vendor_data['vendorClassification'].value_counts()

col1, col2 = st.columns([2,2])

col1.bar_chart(count_vendor)

col1.subheader('Vendor Classification')

col2.bar_chart(count_product)

col2.subheader('Product Classification')






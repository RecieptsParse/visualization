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
import matplotlib.pyplot as plt

with open("data/classified_receipts.json", 'r') as json_file:
    # Load the JSON data
    data = json.load(json_file)


vendor_clasified = dict()

product_classified = dict()

for i, receipt in enumerate(data):
    vendor_class = receipt["ReceiptInfo"]['vendorClassification']
    if vendor_class in vendor_clasified:
        vendor_clasified[vendor_class] +=1
    else:
        vendor_clasified[vendor_class] = 1
    
    products = receipt['ReceiptInfo']['ITEMS']

    for i, items in enumerate(products):
        product_class = items['productClassification']
        if product_class in product_classified:
            product_classified[product_class] +=1
        else:
            product_classified[product_class] =1
    

# print(vendor_clasified)
# print(product_classified)

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
print(df_product_data)



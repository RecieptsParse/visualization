import os
import json
import sys
import subprocess

try:
    subprocess.run(['/bin/bash', 'install_packages.sh'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running shell script: {e}")

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
    

print(vendor_clasified)
print(product_classified)

df_data = []
for entry in data:
    entry_data = entry["ReceiptInfo"]
    df_data.append(entry_data)


df = pd.DataFrame(df_data)

print(df)
print(df.columns)



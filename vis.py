import os
import json
import sys
import subprocess

import ner_evaluate

# try:
#     subprocess.run(['/bin/bash', 'install_packages.sh'], check=True)
# except subprocess.CalledProcessError as e:
#     print(f"Error running shell script: {e}")

import streamlit as st
import pandas as pd
import statistics

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

product_data = []

for i, entry in enumerate(data):
    entry_data = entry['ReceiptInfo']['ITEMS']
    for j, items in enumerate(entry_data):
        items['item_id'] = i
        product_data.append(items)
    
df_product_data = pd.DataFrame(product_data)

df_product_data = df_product_data.drop(columns=['includedItems'])


count_product = df_product_data['productClassification'].value_counts()


count_vendor = df_vendor_data['vendorClassification'].value_counts()

st.markdown("<h1 style='text-align: center;'>Receipt Parse</h1>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([2,2])

col1.subheader(':blue[Vendor Classification]')

col1.bar_chart(count_vendor, color="#1338BE")

col2.subheader(':violet[Product Classification]')

col2.bar_chart(count_product, color="#B200ED")

with st.sidebar:
        st.title("About Us")
        st.write("""Welcome to the final project visulization of ICS 438. Our group is made up of 4 members: Jeremiah Dy, Kylie Higashionna, Grayson Levy, Amanda Nitta.
                 We created a parser to convert receipt data into structured JSON documents adhering to a specified schema utilizing ChatGPT4. We classified each receipt's 
                 vendor and products into predefined categories using a classification method from the FAISS library which employed K-Nearest Neighbors.""")
        st.link_button("OCR to JSON Repository", "https://github.com/RecieptsParse/OCR_TO_JSON")
        st.link_button("Visualization Repository", "https://github.com/RecieptsParse/visualization")

overall_results, overall_results_per_tag = ner_evaluate.get_results()

precision_average_ent_type = statistics.mean([ x['ent_type']['precision'] for x in overall_results])
recall_average_ent_type = statistics.mean( x['ent_type']['recall'] for x in overall_results)
f1_average_ent_type = statistics.mean( x['ent_type']['f1'] for x in overall_results)
correct_average_ent_type = statistics.mean( x['ent_type']['correct'] for x in overall_results)
incorrect_average_ent_type = statistics.mean( x['ent_type']['incorrect'] for x in overall_results)

precision_average_partial_type = statistics.mean([ x['partial']['precision'] for x in overall_results])
recall_average_partial_type = statistics.mean( x['partial']['recall'] for x in overall_results)
f1_average_partial_type = statistics.mean( x['partial']['f1'] for x in overall_results)
correct_average_partial_type = statistics.mean( x['partial']['correct'] for x in overall_results)
incorrect_average_partial_type = statistics.mean( x['partial']['incorrect'] for x in overall_results)

precision_average_exact_type = statistics.mean([ x['exact']['precision'] for x in overall_results])
recall_average_exact_type = statistics.mean( x['exact']['recall'] for x in overall_results)
f1_average_exact_type = statistics.mean( x['exact']['f1'] for x in overall_results)
correct_average_exact_type = statistics.mean( x['exact']['correct'] for x in overall_results)
incorrect_average_exact_type = statistics.mean( x['exact']['incorrect'] for x in overall_results)

precision_average_strict_type = statistics.mean([ x['strict']['precision'] for x in overall_results])
recall_average_strict_type = statistics.mean( x['strict']['recall'] for x in overall_results)
f1_average_strict_type = statistics.mean( x['strict']['f1'] for x in overall_results)
correct_average_exact_type = statistics.mean( x['strict']['correct'] for x in overall_results)
incorrect_average_exact_type = statistics.mean( x['strict']['incorrect'] for x in overall_results)




# Assuming overall_results is defined and structured appropriately

# Define the categories
categories = ['ent_type', 'partial', 'exact', 'strict']

# Initialize a dictionary to hold the averages
averages = {'precision': {}, 'recall': {}, 'f1': {}, 'correct': {}, 'incorrect': {}}

# Compute averages for each category and metric
for category in categories:
    for metric in averages.keys():
        averages[metric][category] = statistics.mean([x[category][metric] for x in overall_results])

# Convert the dictionary to a DataFrame
df = pd.DataFrame(averages)

# Display the DataFrame
print(df)
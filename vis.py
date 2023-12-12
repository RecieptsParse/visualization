import os
import json
import sys
import subprocess

import ner_evaluate

try:
    subprocess.run(['/bin/bash', 'install_packages.sh'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running shell script: {e}")

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

with col1:
    with st.expander("Additional explanation to Vendor Classification"):
        st.write("""
            The chart above shows the frequency of receipts classified into one of six categories of vendors.
            We can see that the Grocery and Supermarket category was the most prevalent with Restaurants and 
            Food services coming in second. Many of the receipts were collected by college students who may buy 
            more at food establishments than at other places of business. 
        """)

col2.subheader(':violet[Product Classification]')

col2.bar_chart(count_product, color="#B200ED")

with col2:
    with st.expander("Additional explanation to Product Classification"):
        st.write("""
            The chart above shows the frequency of items that were classified into one of seventeen categories of 
            products. We can see that the Food product category was the most prevalent with Beverages coming in second. 
            This likely stems from most of the receipts being from Grocery and Supermarkets or Restaurants and Food 
            services establishments.
        """)

with st.sidebar:
        st.title("About Us")
        st.write("""Welcome to the final project visulization of ICS 438. Our group is made up of 4 members: Jeremiah Dy, Kylie Higashionna, Grayson Levy, Amanda Nitta.
                 We created a parser to convert receipt data into structured JSON documents adhering to a specified schema utilizing ChatGPT4. We classified each receipt's 
                 vendor and products into predefined categories using a classification method from the FAISS library which employed K-Nearest Neighbors.
        """)
        st.link_button("OCR to JSON Repository", "https://github.com/RecieptsParse/OCR_TO_JSON")
        st.link_button("Visualization Repository", "https://github.com/RecieptsParse/visualization")

with open("overall_results.json", 'r') as overall_results_data:
    # Load the JSON data
    overall_results = json.load(overall_results_data)

with open('overall_results_per_tag.json','r') as overall_results_per_tag_data:
    overall_results_per_tag = json.load(overall_results_per_tag_data)



precision_average_ent_type = statistics.mean([ x['ent_type']['precision'] for x in overall_results])
recall_average_ent_type = statistics.mean( x['ent_type']['recall'] for x in overall_results)
f1_average_ent_type = statistics.mean( x['ent_type']['f1'] for x in overall_results)
correct_average_ent_type = statistics.mean( x['ent_type']['correct'] for x in overall_results)
incorrect_average_ent_type = statistics.mean( x['ent_type']['incorrect'] for x in overall_results)
partial_average_ent_type = statistics.mean( x['ent_type']['partial'] for x in overall_results)
missed_average_ent_type = statistics.mean( x['ent_type']['missed'] for x in overall_results)
spurious_average_ent_type = statistics.mean( x['ent_type']['spurious'] for x in overall_results)


precision_average_partial_type = statistics.mean([ x['partial']['precision'] for x in overall_results])
recall_average_partial_type = statistics.mean( x['partial']['recall'] for x in overall_results)
f1_average_partial_type = statistics.mean( x['partial']['f1'] for x in overall_results)
correct_average_partial_type = statistics.mean( x['partial']['correct'] for x in overall_results)
incorrect_average_partial_type = statistics.mean( x['partial']['incorrect'] for x in overall_results)
partial_average_partial_type = statistics.mean( x['partial']['partial'] for x in overall_results)
missed_average_partial_type = statistics.mean( x['partial']['missed'] for x in overall_results)
spurious_average_partial_type = statistics.mean( x['partial']['spurious'] for x in overall_results)

precision_average_exact_type = statistics.mean([ x['exact']['precision'] for x in overall_results])
recall_average_exact_type = statistics.mean( x['exact']['recall'] for x in overall_results)
f1_average_exact_type = statistics.mean( x['exact']['f1'] for x in overall_results)
correct_average_exact_type = statistics.mean( x['exact']['correct'] for x in overall_results)
incorrect_average_exact_type = statistics.mean( x['exact']['incorrect'] for x in overall_results)
partial_average_exact_type = statistics.mean( x['exact']['partial'] for x in overall_results)
missed_average_exact_type = statistics.mean( x['exact']['missed'] for x in overall_results)
spurious_average_exact_type = statistics.mean( x['exact']['spurious'] for x in overall_results)

precision_average_strict_type = statistics.mean([ x['strict']['precision'] for x in overall_results])
recall_average_strict_type = statistics.mean( x['strict']['recall'] for x in overall_results)
f1_average_strict_type = statistics.mean( x['strict']['f1'] for x in overall_results)
correct_average_strict_type = statistics.mean( x['strict']['correct'] for x in overall_results)
incorrect_average_strict_type = statistics.mean( x['strict']['incorrect'] for x in overall_results)
partial_average_strict_type = statistics.mean( x['strict']['partial'] for x in overall_results)
missed_average_strict_type = statistics.mean( x['strict']['missed'] for x in overall_results)
spurious_average_strict_type = statistics.mean( x['strict']['spurious'] for x in overall_results)




# Assuming overall_results is defined and structured appropriately

# Define the categories
categories = ['ent_type', 'partial', 'exact', 'strict']

# Initialize a dictionary to hold the averages
averages = {'precision': {}, 'recall': {}, 'f1': {}, 'correct': {}, 'incorrect': {}, 'partial': {}, 'missed': {}, 'spurious': {}}

# Compute averages for each category and metric
for category in categories:
    for metric in averages.keys():
        averages[metric][category] = statistics.mean([x[category][metric] for x in overall_results])

# Convert the dictionary to a DataFrame
df_NER = pd.DataFrame(averages)

# Display the DataFrame
print(df_NER)

st.divider()

st.markdown("<h3 style='text-align: center;'>NER performance</h3>", unsafe_allow_html=True)

st.dataframe(df_NER, use_container_width=True)


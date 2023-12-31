import json
import subprocess

# s

import streamlit as st
import pandas as pd
import statistics
import jsonschema

with open("data/classified_receipts.json", 'r') as json_file:
    # Load the JSON data
    data = json.load(json_file)

# creates dataframe for receipt info with id
vendor_data = []
for i,entry in enumerate(data):
    entry_data = entry["ReceiptInfo"]
    entry_data['entry_id'] = i
    vendor_data.append(entry_data)


df_vendor_data = pd.DataFrame(vendor_data)
df_vendor_data = df_vendor_data.drop(columns=['ITEMS'])

# creates dataframe for products with entry id
product_data = []

for i, entry in enumerate(data):
    entry_data = entry['ReceiptInfo']['ITEMS']
    for j, items in enumerate(entry_data):
        items['entry_id'] = i
        product_data.append(items)
    
df_product_data = pd.DataFrame(product_data)
df_product_data = df_product_data.drop(columns=['includedItems'])

# determine amount for each product classification
count_product = df_product_data['productClassification'].value_counts()

# determine amount for each vendor classification
count_vendor = df_vendor_data['vendorClassification'].value_counts()

st.markdown("<h1 style='text-align: center;'>Receipt Parse</h1>", unsafe_allow_html=True)

st.divider()

# creates plot for vendor classifcation and information expander
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

# creates plot for product classifcation and information expander

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

# creates sidebar explaining project
with st.sidebar:
        st.title("About")
        st.write("""
                 This Dashboard displays how often people purchase particular items through displaying the categorization of 
                 receipt information based on vendor and product.

                 We created a parser to convert receipt data into structured JSON documents keeping all the information consistent/ correct with 
                 how humans view receipts utilizing ChatGPT4. We classified each receipt's vendor and products into predefined categories using a 
                 classification method with K-Nearest Neighbors.

                 Team
                 - Jeremiah Dy
                 - Kylie Higashionna
                 - Grayson Levy
                 - Amanda Nitta

                 Acknowledgement: Fall 2023 Big Data Analytics Course with Dr. Mahdi Belcaid
        """)
        st.link_button("Optical Character Recognition (OCR) - text file to JSON: Repository", "https://github.com/RecieptsParse/OCR_TO_JSON")
        st.link_button("Visualization: Repository", "https://github.com/RecieptsParse/visualization")

# loads in results of NER Evaluate

with open("overall_results.json", 'r') as overall_results_data:
    # Load the JSON data
    overall_results = json.load(overall_results_data)

with open('overall_results_per_tag.json','r') as overall_results_per_tag_data:
    overall_results_per_tag = json.load(overall_results_per_tag_data)


# gets the mean for each metric/ category
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

st.divider()

st.markdown("<h3 style='text-align: center;'> Average Named Entity Recognition (NER) Performance</h3>", unsafe_allow_html=True)

st.dataframe(df_NER, use_container_width=True)



with st.expander("Additional Information for Named Entity Recognition (NER)"):
    st.write("""
        The table above displays how well our JSON creation performed compared to our expected. From the above it can be observed that
             the JSONs were created as expected for the majority.
    """)

st.divider()

st.markdown("<h3 style='text-align: center;'>Breakdown of Product Distribution Among the Vendors</h3>", unsafe_allow_html=True)

with st.expander("Additional Explaination for Breakdown of Product Distribution"):
    st.write("""
        The charts below displays all seventeen different product categories and what type of vendor category people are buying these products from.
    """)

# combines product and vendor dataframes and counts occurences of the combinations
combined_data = df_vendor_data.merge(df_product_data,how="inner",on='entry_id')

grouped_data = combined_data.groupby(['productClassification','vendorClassification'])

count_combined = grouped_data.size().reset_index(name='count')

count_combined_product = count_combined.groupby('productClassification')

product_category = [ 'Food Products',  'Beverages', 'Health And Beauty',  'Clothing And Accessories', 'Electronics',  'Home',  'Outdoor Goods', 'Automotive', 'Toys And Games', 'Sporting Goods', 'Books And Stationery', 'Pharmacy And Health Products', 'Pet Supplies', 'Baby Products', 'Cleaning Supplies', 'Gifts And Miscellaneous', 'Event Tickets']

# creates plots displaying where products are bought per vendor
col1, col2, col3 = st.columns([3,3,3])

i = 0

number_cat = len(product_category)

while i < number_cat:
    if i % 3 == 0:
        st.divider()
        col1, col2, col3 = st.columns([3,3,3])
        arr_cols = [col1,col2,col3]
    for j in range(len(arr_cols)):
        count_product_info = count_combined_product.get_group(product_category[i])
        count_product_info = count_product_info.drop(columns='productClassification', index=None)
        arr_cols[j].subheader(f':black[{product_category[i]}]')
        arr_cols[j].bar_chart(count_product_info.set_index('vendorClassification'), color="#B7C5FF")
        i+=1
        if i >= number_cat:
            break
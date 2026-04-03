# =========================
# SETUP
# =========================

import os
import pandas as pd
import numpy as np
import warnings
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Set pandas dataframe visual settings

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

# Remove warning messages from the output.

warnings.simplefilter("ignore")

#Load CSV file into pandas df

df = pd.read_csv("heartdata_recoded.csv")

# =========================
# TRANSACTION ENCODING
# =========================

transactions = [[f"{col}={val}" for col, val in row.items()] for index, row in df.iterrows()]

# This command opens an instance of transaction encoder. Just like opening a blank excel sheet

te = TransactionEncoder()

# Fit method finds out distinct items (vocabulary) and then convert them into a binary sparse matrix.

te_array = te.fit(transactions).transform(transactions)

# We then convert this sparse matrix into a data frame with each item as a column name.

df_trans = pd.DataFrame(te_array, columns=te.columns_)

# =========================
# APRIORI
# =========================

frequent_items = apriori(
    df_trans,
    min_support=0.2,
    use_colnames=True
)

#Association Rules

heartdisease_rule11 = association_rules(
    frequent_items,
    metric="confidence",
    min_threshold=0.7
)   
#Add total rule ["length"]
    
heartdisease_rule11["length"] = heartdisease_rule11['antecedents'].apply(len) + heartdisease_rule11['consequents'].apply(len)

#Keep only association rules with more than 3 items
    
heartdisease_rule11_filtered = heartdisease_rule11[heartdisease_rule11["length"]  >= 3]

# Filter rules by target class
    
buff_rules = heartdisease_rule11_filtered[heartdisease_rule11_filtered["consequents"] == {'class=buff'}]

sick_rules = heartdisease_rule11_filtered[heartdisease_rule11_filtered["consequents"] == {'class=sick'}]

# =========================
# WRITE OUTPUT FILES
# =========================

# Write rules directly

buff_rules.to_csv(
    "buff_rules.csv",
    sep="|",
    index=False
)

sick_rules.to_csv(
    "sick_rules.csv",
    sep="|",
    index=False
)

print("Done. Files created: buff_rules.csv and sick_rules.csv")

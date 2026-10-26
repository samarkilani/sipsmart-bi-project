"""
SipSmart Drink Retail Store - Data Cleaning Script
Description: Loads raw CSV datasets, handles missing/null values,
and standardizes date formats for downstream transformations.
"""

import pandas as pd
import numpy as np

def clean_data():
    print("--- Starting Data Cleaning Phase ---")
    
    # 1. Load raw datasets from the data directory
    sales = pd.read_csv('../data/sales.csv')
    purchases = pd.read_csv('../data/purchases.csv')
    beginning_inventory = pd.read_csv('../data/beginning_inventory.csv')
    end_inventory = pd.read_csv('../data/end_inventory.csv')

    # 2. Clean Sales Data: Replace missing numerical values with safe defaults (0)
    sales['SalesQuantity'] = sales['SalesQuantity'].fillna(0)
    sales['SalesDollars'] = sales['SalesDollars'].fillna(0.0)
    sales['SalesPrice'] = sales['SalesPrice'].fillna(0.0)
    
    # 3. Standardize and parse date strings into datetime objects safely
    sales['SalesDate'] = pd.to_datetime(sales['SalesDate'], format='%d-%m-%Y', errors='coerce')
    purchases['ReceivingDate'] = pd.to_datetime(purchases['ReceivingDate'], format='%d-%m-%Y', errors='coerce')

    print("Data cleaning completed successfully.")
    return sales, purchases, beginning_inventory, end_inventory

if __name__ == "__main__":
    clean_data()

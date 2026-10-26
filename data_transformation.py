"""
SipSmart Drink Retail Store - Data Transformation & ID Mapping Script
Description: Takes cleaned data, generates dimension tables, builds the 
Date dimension, maps foreign keys, and computes fact metrics like Stock Turnover.
"""

import pandas as pd
import numpy as np
from data_cleaning import clean_data

def transform_data():
    print("--- Starting Data Transformation & Dimension Mapping Phase ---")
    
    # Import cleaned datasets from the cleaning module
    sales, purchases, beginning_inventory, end_inventory = clean_data()

    # =================================================================
    # Step 1: Create Dimension Tables & Map IDs
    # =================================================================
    
    # Create ProductDim from unique brands
    product_dim = beginning_inventory[['Brand']].drop_duplicates().reset_index(drop=True)
    product_dim['ProductId'] = range(1, len(product_dim) + 1)

    # Create StoreDim from unique stores and cities
    store_dim = beginning_inventory[['Store', 'City']].drop_duplicates().reset_index(drop=True)
    store_dim['StoreId'] = range(1, len(store_dim) + 1)

    # Create VendorDim using vendor numbers and names
    vendor_dim = purchases[['Vendor Number', 'VendorName']].drop_duplicates().reset_index(drop=True)
    vendor_dim.rename(columns={'VendorNumber': 'VendorId'}, inplace=True)

    # Helper function to extract temporal parts for DateDim
    def extract_date_parts(date_column):
        date_column = pd.Series(date_column)
        return pd.DataFrame({
            'DateId': range(1, len(date_column) + 1),
            'Day': date_column.dt.day,
            'Month': date_column.dt.month,
            'Quarter': date_column.dt.quarter,
            'Year': date_column.dt.year,
            'Date': date_column
        })

    # Combine sales and purchase dates to build a unified DateDim
    dates = pd.concat([sales['SalesDate'], purchases['ReceivingDate']])
    date_dim = extract_date_parts(pd.to_datetime(dates.dropna().unique(), format='%d-%m-%Y', errors='coerce'))

    # =================================================================
    # Step 2: Build FactSales Table
    # =================================================================
    sales_fact = sales.copy()
    sales_fact = sales_fact.merge(product_dim, on='InventoryId', how='left')
    sales_fact = sales_fact.merge(store_dim, on='Store', how='left')
    sales_fact['SalesDate'] = pd.to_datetime(sales_fact['SalesDate'], format='%d-%m-%Y', errors='coerce')
    
    # Merge with DateDim and VendorDim to associate foreign keys
    sales_fact = sales_fact.merge(date_dim, left_on='SalesDate', right_on='Date', how='left')
    sales_fact = sales_fact.merge(vendor_dim, on='VendorName', how='left')

    # Handle unmapped foreign keys by assigning default fallback values (-1)
    sales_fact['StoreId'] = sales_fact['StoreId'].fillna(-1).astype(int)
    sales_fact['ProductId'] = sales_fact['ProductId'].fillna(-1).astype(int)
    sales_fact['DateId'] = sales_fact['DateId'].fillna(-1).astype(int)

    # =================================================================
    # Step 3: Build FactInventory Table & Calculate Metrics
    # =================================================================
    inventory_fact = beginning_inventory.merge(end_inventory, on=['InventoryId', 'Store'], suffixes=('_start', '_end'), how='outer')
    inventory_fact = inventory_fact.merge(product_dim, on='InventoryId', how='left')
    inventory_fact = inventory_fact.merge(store_dim, on='Store', how='left')

    inventory_fact['onHandStart'] = inventory_fact['onHand_start'].fillna(0).astype(int)
    inventory_fact['onHandEnd'] = inventory_fact['onHand_end'].fillna(0).astype(int)

    # Aggregate stock received and sold metrics
    stock_received = purchases.groupby('InventoryId').size().reindex(inventory_fact['InventoryId'], fill_value=0)
    inventory_fact['StockReceived'] = stock_received.values

    stock_sold = sales.groupby('InventoryId')['SalesQuantity'].sum().reindex(inventory_fact['InventoryId'], fill_value=0)
    inventory_fact['StockSold'] = stock_sold.values

    # Calculate Stock Turnover securely (protecting against division by zero)
    inventory_fact['StockTurnover'] = (
        inventory_fact['StockSold'] / inventory_fact['onHandStart'].replace(0, np.nan)
    ).fillna(0).round(2)

    print("Transformation, ID mapping, and calculations completed successfully.")

if __name__ == "__main__":
    transform_data()

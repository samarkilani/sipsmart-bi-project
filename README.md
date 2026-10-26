# 🍷 SipSmart Drink Retail Store - Business Intelligence & Data Warehouse

An end-to-end Business Intelligence (BI) and Data Warehouse project built for **SipSmart Drink Retail Store**[cite: 2]. This repository implements a robust dimensional data model utilizing a **Fact Constellation Schema** to analyze retail sales performance, inventory turnover, and vendor metrics[cite: 2, 4].

## 🏗️ Architecture & Dimensional Model
The data warehouse is structured around a fact constellation schema to optimize analytical queries and reporting:
* **Dimension Tables:** 
  * `ProductDim`: Stores unique product and brand details[cite: 2, 3].
  * `StoreDim`: Stores store locations and city details[cite: 2, 3].
  * `DateDim`: Manages temporal hierarchies (Day, Month, Quarter, Year)[cite: 2, 3].
  * `VendorDim`: Tracks supplier and vendor information[cite: 2, 3].
* **Fact Tables:** 
  * `FactSales`: Tracks sales quantities, dollars, and pricing[cite: 2, 4].
  * `FactInventory`: Tracks beginning/ending inventory levels, stock received, stock sold, and calculated **Stock Turnover** rates[cite: 2, 4].

## 📂 Repository Structure
* `schema.sql`: Complete MySQL script to set up the database and relational table constraints.
* `data_cleaning.py`: Python script handling raw dataset preprocessing, missing value imputation, and date parsing.
* `data_transformation.py`: Python script managing dimension mapping, foreign key assignments, and fact table metrics.
* `visualization/`: Contains exports and reports from the Looker dashboard layer.

## 📊 Business Intelligence & Visualization
* Built interactive dashboards and KPI reports using **Looker / Looker Studio** to track executive-level insights, including sales trends, inventory efficiency, and supplier contributions.

## 🛠️ Tech Stack
* **Database & Management:** MySQL, MySQL Workbench[cite: 2]
* **Data Processing & ETL:** Python (Pandas, NumPy)
* **Visualization:** Looker / Looker Studio
* **Version Control:** Git & GitHub

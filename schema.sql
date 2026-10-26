-- =====================================================================
-- SipSmart Drink Retail Store - Database Schema & Data Warehouse Setup
-- Description: Creates the 'Drinks' database, dimensional tables, 
-- and fact tables with primary and foreign key constraints.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS Drinks;
USE Drinks;

-- -----------------------------------------------------------------
-- 1. Dimension Tables
-- -----------------------------------------------------------------

-- Product Dimension: Stores unique brand information
CREATE TABLE IF NOT EXISTS ProductDim (
    ProductId INT PRIMARY KEY AUTO_INCREMENT,
    Brand VARCHAR(255)
);

-- Store Dimension: Stores unique store locations and cities
CREATE TABLE IF NOT EXISTS StoreDim (
    StoreId INT PRIMARY KEY AUTO_INCREMENT,
    Store VARCHAR(255),
    City VARCHAR(255)
);

-- Date Dimension: Stores temporal attributes (Day, Month, Quarter, Year)
CREATE TABLE IF NOT EXISTS DateDim (
    DateId INT PRIMARY KEY AUTO_INCREMENT,
    Day INT,
    Month INT,
    Quarter INT,
    Year INT
);

-- Vendor Dimension: Stores unique supplier/vendor names
CREATE TABLE IF NOT EXISTS VendorDim (
    VendorId INT PRIMARY KEY AUTO_INCREMENT,
    VendorName VARCHAR(50) UNIQUE
);

-- -----------------------------------------------------------------
-- 2. Fact Tables
-- -----------------------------------------------------------------

-- Inventory Fact Table: Tracks stock levels, receipts, sales, and turnover
CREATE TABLE IF NOT EXISTS FactInventory (
    InventoryId INT PRIMARY KEY AUTO_INCREMENT,
    onHandStart INT,
    onHandEnd INT,
    StockReceived INT,
    StockSold INT,
    StockTurnover DECIMAL (10,2),
    StoreId INT,
    ProductId INT,
    DateId INT,
    VendorId INT,
    FOREIGN KEY (StoreId) REFERENCES StoreDim (StoreId),
    FOREIGN KEY (ProductId) REFERENCES ProductDim (ProductId),
    FOREIGN KEY (DateId) REFERENCES DateDim (DateId),
    FOREIGN KEY (VendorId) REFERENCES VendorDim (VendorId)
);

-- Sales Fact Table: Tracks retail sales quantities, prices, and revenue
CREATE TABLE IF NOT EXISTS FactSales (
    SalesId INT PRIMARY KEY AUTO_INCREMENT,
    SalesQuantity INT,
    SalesDollars DECIMAL (10,2),
    SalesPrice DECIMAL (10,2),
    StoreId INT,
    ProductId INT,
    DateId INT,
    VendorId INT,
    FOREIGN KEY (StoreId) REFERENCES StoreDim (StoreId),
    FOREIGN KEY (ProductId) REFERENCES ProductDim (ProductId),
    FOREIGN KEY (DateId) REFERENCES DateDim (DateId),
    FOREIGN KEY (VendorId) REFERENCES VendorDim (VendorId)
);

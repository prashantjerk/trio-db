CREATE DATABASE Opurchase;
use Opurchase;
SET FOREIGN_KEY_CHECKS = 1;

-- drop database Opurchase;
CREATE TABLE Customer (
    customer_Id INT AUTO_INCREMENT PRIMARY KEY,
    fName VARCHAR(50),
    lName VARCHAR(50),
    DOB DATE,
    street VARCHAR(100),
    zipCode CHAR(5),
    city VARCHAR(50),
    country VARCHAR(50),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE BankInfo (
    account_Id INT AUTO_INCREMENT PRIMARY KEY,
    customer_Id INT,
    bankName VARCHAR(100),
    accountNb VARCHAR(50),
    FOREIGN KEY (customer_Id) REFERENCES Customer(customer_Id)
);

CREATE TABLE Supplier (
   supplier_Id INT AUTO_INCREMENT PRIMARY KEY,
   supplierName VARCHAR(50),
   Address VARCHAR (100)
);

CREATE TABLE Item (
    item_Id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2),
    supplier_Id INT,
    FOREIGN KEY (supplier_Id) REFERENCES Supplier(supplier_Id)
);

CREATE TABLE Cart (
    cart_Id INT AUTO_INCREMENT PRIMARY KEY,
    customer_Id INT,
    item_Id INT,
    quantity INT,
    FOREIGN KEY (customer_Id) REFERENCES Customer(customer_Id),
    FOREIGN KEY (item_Id) REFERENCES Item(item_Id)
);

CREATE TABLE Discount (
    discount_Id INT AUTO_INCREMENT PRIMARY KEY,
    minPrice DECIMAL(10, 2),
    maxPrice DECIMAL(10, 2),
    discountValue DECIMAL(5, 2)
);

CREATE TABLE Bill (
    bill_Id INT AUTO_INCREMENT PRIMARY KEY,
    customer_Id INT,
    totalAmount DECIMAL(10, 2),
    FOREIGN KEY (customer_Id) REFERENCES Customer(customer_Id)
);

CREATE TABLE BillItems (
    billItem_Id INT AUTO_INCREMENT PRIMARY KEY,
    bill_Id INT,
    item_Id INT,
    quantity INT,
    priceAfterDiscount DECIMAL(10, 2),
    discount_Id INT,
    FOREIGN KEY (bill_Id) REFERENCES Bill(bill_Id),
    FOREIGN KEY (item_Id) REFERENCES Item(item_Id),
    FOREIGN KEY (discount_Id) REFERENCES Discount(discount_Id)
);

CREATE TABLE Manager (
    managerId INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL DEFAULT 'admin',
    password VARCHAR(255) NOT NULL DEFAULT 'admin'
);

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
    balance DECIMAL(10, 2),
    FOREIGN KEY (customer_Id) REFERENCES Customer(customer_Id)
);

CREATE TABLE Supplier (
   supplier_Id INT AUTO_INCREMENT PRIMARY KEY,
   supplierName VARCHAR(50),
   Address VARCHAR (100)
);

CREATE TABLE Item (
    item_Id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
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


-- trigger -- NO 5
DELIMITER $$

CREATE TRIGGER ApplyDiscountOnBill
AFTER INSERT ON Bill
FOR EACH ROW
BEGIN
    DECLARE applicableDiscount DECIMAL(5, 2);

    -- Retrieve the applicable discount value from the Discount table
    SELECT discountValue
    INTO applicableDiscount
    FROM Discount
    WHERE NEW.totalAmount > minPrice
      AND (maxPrice IS NULL OR NEW.totalAmount <= maxPrice)
    ORDER BY minPrice DESC
    LIMIT 1;

    -- Apply the discount to the totalAmount if an applicable discount is found
    IF applicableDiscount IS NOT NULL THEN
        UPDATE Bill
        SET totalAmount = NEW.totalAmount * (1 - applicableDiscount)
        WHERE bill_Id = NEW.bill_Id;
    END IF;
END$$

DELIMITER ;


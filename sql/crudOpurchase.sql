
-- NO 4
INSERT INTO Customer (fName, lName, DOB, street, zipCode, city, country, username, password)
VALUES 
('John', 'Doe', '1990-01-01', '123 Main St', '12345', 'Springfield', 'USA', 'jdoe', 'password123'),
('Alice', 'Smith', '1985-05-05', '456 Elm St', '54321', 'Shelbyville', 'USA', 'asmith', 'securepass'),
('Bob', 'Brown', '1992-03-03', '789 Pine St', '23456', 'Centerville', 'USA', 'bbrown', 'mypassword'),
('Clara', 'Johnson', '1988-07-07', '321 Maple St', '67890', 'Riverdale', 'USA', 'cjohnson', 'clara123'),
('David', 'Lee', '1995-10-10', '654 Oak St', '34567', 'Hillside', 'USA', 'dlee', 'dlee987');

INSERT INTO BankInfo (customer_Id, bankName, accountNb)
VALUES 
(1, 'Bank of America', '1234567890'),
(2, 'Chase Bank', '9876543210'),
(3, 'Wells Fargo', '1122334455'),
(4, 'Citi Bank', '6677889900'),
(5, 'HSBC', '5566778899');

INSERT INTO Supplier (supplierName, Address)
VALUES 
('Supplier A', '123 Market St'),
('Supplier B', '456 Commerce Ave'),
('Supplier C', '789 Trade Blvd'),
('Supplier D', '321 Business Rd'),
('Supplier E', '654 Industry Way');

INSERT INTO Item (name, price, supplier_Id)
VALUES 
('Laptop', 899.99, 1),
('Mouse', 25.00, 2),
('Keyboard', 45.00, 3),
('Monitor', 150.00, 4),
('Printer', 200.00, 5);

INSERT INTO Cart (customer_Id, item_Id, quantity)
VALUES 
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 1),
(5, 5, 2);

INSERT INTO Discount (minPrice, maxPrice, discountValue)
VALUES 
(50, 150, 0.05),
(100.01, 150, 0.10),
(150.01, 200, 0.15),
(200.01, 300, 0.20),
(300.01, 500, 0.25);

INSERT INTO Manager (userName, password)
VALUES 
('admin', 'admin');

SELECT * FROM Bill;

INSERT INTO Bill (bill_Id, customer_Id, totalAmount)
VALUES 
(1, 1, 1000.00),
(2, 2, 500.00),
(3, 3, 300.00),
(4, 4, 800.00),
(5, 5, 1200.00);

INSERT INTO BillItems (billItem_Id, bill_Id, item_Id, quantity, priceAfterDiscount, discount_Id)
VALUES 
(1, 1, 1, 1, 809.99, 4),
(2, 2, 2, 2, 45.00, 2),
(3, 3, 3, 3, 114.75, 3),
(4, 4, 4, 1, 135.00, 3),
(5, 5, 5, 2, 160.00, 4);

select * from BillItems;
select * from customer;
select * from bankInfo;
select * from cart;
select * from item;
select * from bill;
select * from discount;

-- trigger -- NO 5

DELIMITER 

CREATE TRIGGER ApplyDiscountOnBill
AFTER INSERT ON Bill
FOR EACH ROW
BEGIN
    DECLARE discountId INT;

    -- Check if a 10% discount for the range over 100 USD exists in the Discount table
    SELECT discount_Id INTO discountId
    FROM Discount
    WHERE minPrice <= NEW.totalAmount
      AND (maxPrice IS NULL OR maxPrice >= NEW.totalAmount)
      AND discountValue = 0.10;

    -- If no such discount exists, insert it into the Discount table
    IF discountId IS NULL THEN
        INSERT INTO Discount (minPrice, maxPrice, discountValue)
        VALUES (100.01, NULL, 0.10);

        -- Get the newly inserted discountId
        SET discountId = LAST_INSERT_ID();
    END IF;

    -- Apply a 10% discount if the totalAmount exceeds 100 USD
    IF NEW.totalAmount > 100 THEN
        UPDATE Bill
        SET totalAmount = NEW.totalAmount * (1 - 0.10)
        WHERE bill_Id = NEW.bill_Id;
    END IF;
END;

DELIMITER ;


SELECT * FROM Bill WHERE customer_Id = 1;
SELECT * FROM Discount;

-- index No 6

CREATE INDEX idx_lName ON Customer(lName);
SELECT * FROM Customer WHERE lName = 'Smith';

-- NO 7
-- bill of the customer

SELECT b.bill_Id, b.totalAmount, b.customer_Id, c.fName, c.lName
FROM Bill b
JOIN Customer c ON b.customer_Id = c.customer_Id
WHERE c.lName = 'Smith';

-- avg purchase per zip -- NO 8

CREATE VIEW AvgPurchasesPerZip AS
SELECT c.zipCode, AVG(b.totalAmount) AS avgPurchase
FROM Customer c
JOIN Bill b ON c.customer_Id = b.customer_Id
GROUP BY c.zipCode;

SELECT * FROM AvgPurchasesPerZip;

-- No 9
-- Creating a new bill

INSERT INTO Bill (customer_Id, totalAmount)
VALUES (1, 0.00);

-- Getting the newly created bill_Id
SET @billId = LAST_INSERT_ID();

-- Adding items to the bill
INSERT INTO BillItems (bill_Id, item_Id, quantity, priceAfterDiscount, discount_Id)
VALUES 
(@billId, 1, 1, 809.99, 4), 
(@billId, 2, 2, 22.50, 1); 

-- Updating totalAmount in the Bill table
UPDATE Bill
SET totalAmount = (
    SELECT SUM(priceAfterDiscount * quantity)
    FROM BillItems
    WHERE bill_Id = @billId
)
WHERE bill_Id = @billId;

-- Verifying the final Bill
SELECT * FROM Bill WHERE bill_Id = @billId;
SELECT * FROM BillItems WHERE bill_Id = @billId;

Select * from bill;


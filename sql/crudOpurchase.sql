use Opurchase;

INSERT INTO Customer (fName, lName, DOB, street, zipCode, city, country, username, password)
VALUES
('John', 'Doe', '1990-01-01', '123 Elm St', '10001', 'New York', 'USA', 'johndoe', 'password123'),
('Jane', 'Smith', '1985-02-02', '456 Oak Ave', '20002', 'Washington', 'USA', 'janesmith', 'mypassword'),
('Mike', 'Brown', '1992-03-03', '789 Pine Rd', '30003', 'Atlanta', 'USA', 'mikebrown', 'securepass');

INSERT INTO BankInfo (customer_Id, bankName, accountNb, balance)
VALUES
(4, 'Chase', '9998887766', 1200.00);


INSERT INTO BankInfo (customer_Id, bankName, accountNb, balance)
VALUES
(1, 'Chase', '123456789', 1000.00),
(2, 'Bank of America', '987654321', 1200.00),
(3, 'Wells Fargo', '112233445', 1500.00);

INSERT INTO Supplier (supplierName, Address)
VALUES
('Tech Supplies', '101 Tech Lane'),
('Gadget Hub', '202 Gadget Blvd'),
('Furniture Mart', '303 Home St');

INSERT INTO Item (name, price, quantity, supplier_Id)
VALUES
('Laptop', 800.00, 10, 1),
('Smartphone', 600.00, 15, 1),
('Desk', 150.00, 20, 3),
('Chair', 100.00, 30, 3),
('Headphones', 50.00, 25, 2);

INSERT INTO Cart (customer_Id, item_Id, quantity)
VALUES
(1, 1, 1), -- read as: John adds 1 Laptop
(1, 5, 2), 
(2, 2, 1), 
(2, 3, 1), 
(3, 4, 3); 

select * from cart;
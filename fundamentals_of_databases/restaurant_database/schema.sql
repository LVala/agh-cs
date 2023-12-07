CREATE TABLE Categories (
categoryId int NOT NULL IDENTITY (1,1),
categoryName varchar(100) NOT NULL,
CONSTRAINT Categories_pk PRIMARY KEY (categoryId)
);

CREATE TABLE Tables (
tableId int NOT NULL IDENTITY(1,1),
isActive bit NOT NULL DEFAULT 1,
CONSTRAINT Tables_pk PRIMARY KEY (tableId)
);

CREATE TABLE Customers (
customerId int NOT NULL IDENTITY (1,1),
firstName varchar(100) NOT NULL,
lastName varchar(100) NOT NULL,
companyName varchar(100) NULL,
phone varchar(15) NOT NULL,
address varchar(100) NULL,
city varchar(100) NULL,
postalCode varchar(10) NULL,
email varchar(100) NULL CHECK(email IS NULL OR email LIKE '%_@%_.%_'),
takesPeriodicInvoice bit NOT NULL DEFAULT 0,
CONSTRAINT Customers_pk PRIMARY KEY (customerId)
);

CREATE TABLE Employees (
employeeId int NOT NULL IDENTITY(1,1),
firstName varchar(100) NOT NULL,
lastName varchar(100) NOT NULL,
birthDate smalldatetime NOT NULL CHECK(birthDate <= GETDATE()),
hireDate smalldatetime NOT NULL CHECK(hireDate <= GETDATE()),
position varchar(100) NOT NULL,
phone varchar(15) NOT NULL,
address varchar(100) NOT NULL,
city varchar(100) NOT NULL,
postalCode varchar(10) NOT NULL,
reportsTo int NULL,
CONSTRAINT Employees_pk PRIMARY KEY (employeeId)
);
-- Reference: Employees_Employees (table: Employees)
ALTER TABLE Employees ADD CONSTRAINT Employees_Employees
FOREIGN KEY (reportsTo)
REFERENCES Employees (employeeId);

CREATE TABLE Dishes (
itemId int NOT NULL IDENTITY(1,1),
categoryId int NOT NULL,
itemName varchar(100) NOT NULL,
itemPrice money NOT NULL CHECK (itemPrice > 0),
servingSize int NULL,
itemPhoto image NULL,
description varchar(255) NULL,
isActive bit NOT NULL DEFAULT 0,
CONSTRAINT Dishes_pk PRIMARY KEY (itemId)
);
-- Reference: Menu_Categories (table: Dishes)
ALTER TABLE Dishes ADD CONSTRAINT Menu_Categories
FOREIGN KEY (categoryId)
REFERENCES Categories (categoryId);

CREATE TABLE Menus (
menuId int NOT NULL IDENTITY(1,1),
inDate smalldatetime NOT NULL CHECK(inDate > GETDATE()),
outDate smalldatetime NOT NULL CHECK(outDate > GETDATE()),
isValid bit NOT NULL DEFAULT 0,
CONSTRAINT Menus_pk PRIMARY KEY (menuId)
);

CREATE TABLE MenuDetails (
menuId int NOT NULL,
itemId int NOT NULL,
CONSTRAINT MenuDetails_pk PRIMARY KEY (menuId,itemId)
);
-- Reference: Dishes_MenuDetails (table: MenuDetails)
ALTER TABLE MenuDetails ADD CONSTRAINT Dishes_MenuDetails
FOREIGN KEY (itemId)

CREATE TABLE Orders (
orderId int NOT NULL IDENTITY(1,1),
customerId int NOT NULL,
employeeId int NOT NULL,
orderDate smalldatetime NOT NULL CHECK(orderDate <= GETDATE()),
receiveDate smalldatetime NOT NULL CHECK(receiveDate >= GETDATE()),
isPaid bit NOT NULL,
takeOut bit NOT NULL,
discount decimal(3,2) NOT NULL CHECK(discount BETWEEN 0.00 AND 1.00),
invoiceId int NULL,
CONSTRAINT Orders_pk PRIMARY KEY (orderId)
);
-- Reference: Orders_Customers (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Customers
FOREIGN KEY (customerId)
REFERENCES Customers (customerId);
-- Reference: Orders_Invoices (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Invoices
FOREIGN KEY (invoiceId)
REFERENCES Invoices (invoiceId);
-- Reference: Orders_Employees (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Employees
FOREIGN KEY (employeeId)
REFERENCES Employees (employeeId);

CREATE TABLE OrderDetails (
orderId int NOT NULL,
itemId int NOT NULL,
itemPrice money NOT NULL CHECK(itemPrice > 0),
quantity int NOT NULL CHECK(quantity > 0),
CONSTRAINT OrderDetails_pk PRIMARY KEY (orderId)
);
-- Reference: Dishes_OrderDetails (table: OrderDetails)
ALTER TABLE OrderDetails ADD CONSTRAINT Dishes_OrderDetails
FOREIGN KEY (itemId)
REFERENCES Dishes (itemId);
-- Reference: OrderDetails_Orders (table: OrderDetails)
ALTER TABLE OrderDetails ADD CONSTRAINT OrderDetails_Orders
FOREIGN KEY (orderId)
REFERENCES Orders (orderId);

CREATE TABLE Reservations (
reservationId int NOT NULL IDENTITY(1,1),
orderId int NOT NULL,
reservationDoneDate smalldatetime NOT NULL CHECK(reservationDoneDate <= GETDATE()),
reservationDate smalldatetime NOT NULL CHECK(reservationDate >= GETDATE()),
numberOfGuests int NOT NULL CHECK (numberOfGuests > 0),
CONSTRAINT Reservations_pk PRIMARY KEY (reservationId)
);
-- Reference: Orders_Reservations (table: Reservations)
ALTER TABLE Reservations ADD CONSTRAINT Orders_Reservations
FOREIGN KEY (orderId)
REFERENCES Orders (orderId);

CREATE TABLE ReservationDetails (
reservationId int NOT NULL,
tableId int NOT NULL,
CONSTRAINT ReservationDetails_pk PRIMARY KEY (reservationId,tableId)
);
-- Reference: ReservationDetails_Reservations (table: ReservationDetails)
ALTER TABLE ReservationDetails ADD CONSTRAINT ReservationDetails_Reservations
FOREIGN KEY (reservationId)
REFERENCES Reservations (reservationId);
-- Reference: ReservationDetails_Tables (table: ReservationDetails)
ALTER TABLE ReservationDetails ADD CONSTRAINT ReservationDetails_Tables
FOREIGN KEY (tableId)
REFERENCES Tables (tableId);

CREATE TABLE Factors (
factorsId int NOT NULL,
WZ int NOT NULL,
WK int NOT NULL,
Z1 int NOT NULL,
K1 int NOT NULL,
R1 decimal(3,2) NOT NULL CHECK(R1 BETWEEN 0.00 AND 1.00),
K2 int NOT NULL,
R2 decimal(3,2) NOT NULL CHECK(R2 BETWEEN 0.00 AND 1.00),
D1 int NOT NULL,
CONSTRAINT Factors_pk PRIMARY KEY (factorsId)
);

CREATE TABLE Discounts (
discountId int NOT NULL IDENTITY (1,1),
customerId int NOT NULL,
discountType varchar(20) NOT NULL CHECK(discountType IN ('lifetime', 'temporary')),
startDate smalldatetime NOT NULL CHECK(startDate <= GETDATE()),
wasUsed bit NULL,
CONSTRAINT Discounts_pk PRIMARY KEY (discountId)
);
-- Reference: Customers_Discounts (table: Discounts)
ALTER TABLE Discounts ADD CONSTRAINT Customers_Discounts
FOREIGN KEY (customerId)
REFERENCES Customers (customerId);

CREATE TABLE Invoices (
invoiceId int NOT NULL IDENTITY(1,1),
invoiceNumber int NOT NULL UNIQUE,
invoiceDate smalldatetime NOT NULL CHECK(invoiceDate <= GETDATE()),
customerId int NOT NULL,
address varchar(100) NOT NULL,
city varchar(100) NOT NULL,
postalCode varchar(10) NOT NULL,
isPeriodic bit NOT NULL,
CONSTRAINT Invoices_pk PRIMARY KEY (invoiceId)
);
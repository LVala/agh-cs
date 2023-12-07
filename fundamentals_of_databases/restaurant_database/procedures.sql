CREATE PROCEDURE MenuOfTheDay @date SMALLDATETIME = NULL
AS
IF (@date = NULL)
BEGIN
SET @date = GETDATE()
END
SELECT D.itemId, D.categoryId, D.itemName,
D.itemPrice, D.servingSize, D.itemPhoto,
D.description
FROM dbo.Dishes AS D
INNER JOIN dbo.MenuDetails AS MD
ON D.itemId = MD.itemId
INNER JOIN dbo.Menus AS M
ON MD.menuId = M.menuId
WHERE @date BETWEEN M.inDate AND M.outDate

CREATE PROCEDURE InsertToMenu
@menuId INT,
@itemId INT
AS
BEGIN
IF (NOT EXISTS(SELECT * FROM Menus WHERE @menuId = menuId))
BEGIN
RAISERROR ('No such menuId', -1, -1)
RETURN
END
IF (NOT EXISTS(SELECT * FROM Dishes WHERE @itemId = itemId))
BEGIN
RAISERROR ('No such itemId', -1, -1)
RETURN
END
INSERT INTO MenuDetails(menuId, itemId)
VALUES (@menuId, @itemId)
END

CREATE PROCEDURE ValidateMenu @menuId INT
AS
BEGIN
IF (NOT EXISTS(SELECT menuId FROM Menus WHERE menuId = @menuId))
BEGIN
RAISERROR ('No such menuId', -1, -1)
RETURN
END
IF (2 * (SELECT COUNT(*) FROM DishesFromLastWeeks) < (SELECT COUNT(*) – tu jest błąd
FROM MenuDetails
WHERE menuId = @menuId))
BEGIN
UPDATE Menus SET isValid = 1 WHERE menuId = @menuId
END
ELSE
BEGIN
RAISERROR ('Menu is not valid', -1, -1)
END
END

CREATE PROCEDURE CreateMenu @inDate SMALLDATETIME,
@outDate SMALLDATETIME
AS
BEGIN
IF (DATEDIFF(DAY, @inDate, @outDate) > 14 OR DATEDIFF(DAY, @inDate, @outDate) < 0)
BEGIN
RAISERROR ('Wrong outDate or inDate', -1, -1)
RETURN
END
INSERT INTO Menus(inDate, outDate)
VALUES (@inDate, @outDate)
END

CREATE PROCEDURE AddNewOrder @custemerId INT,
@employeeId INT,
@orderDate SMALLDATETIME,
@receiveDate SMALLDATETIME,
@isPaid BIT,
@takeOut BIT,
@discountType VARCHAR(20)
AS
BEGIN
IF (@discountType NOT LIKE 'lifetime' OR @discountType NOT LIKE 'temporary')
BEGIN
RAISERROR ('No such discount type', -1, -1)
RETURN
END
IF (@orderDate > @receiveDate)
BEGIN
RAISERROR ('Wrong orderDate or receiveDate', -1, -1)
RETURN
END
IF (NOT EXISTS(SELECT customerId FROM Customers WHERE customerId = @custemerId))
BEGIN
RAISERROR ('No such customerId', -1, -1)
RETURN
END
IF (NOT EXISTS(SELECT employeeId FROM Employees WHERE employeeId = @employeeId))
BEGIN
RAISERROR ('No such employeeId', -1, -1)
RETURN
END
IF (NOT EXISTS(SELECT discountId
FROM Discounts
WHERE customerId = @custemerId
AND discountType = @discountType
AND (wasUsed = NULL OR wasUsed = 0)))
BEGIN
RAISERROR ('Customer does not have such discount', -1, -1)
RETURN
END
DECLARE @discount DECIMAL(3, 2)
IF (@discountType LIKE 'lifetime')
BEGIN
SET @discount = (SELECT R1 FROM Factors)
END
ELSE
BEGIN TRANSACTION [Tran1]
BEGIN TRY
BEGIN
DECLARE @discountId INT;
SET @discountId = (SELECT TOP 1 discountId
FROM Discounts
WHERE customerId = @custemerId
AND discountType = @discountType
AND wasUsed = 0
AND DATEDIFF(DAY, startDate, GETDATE()) < (SELECT D1 FROM Factors))
UPDATE Discounts SET wasUsed = 1 WHERE @discountId = discountId
SET @discount = (SELECT R2 FROM Factors)
END
INSERT INTO Orders(customerId, employeeId, orderDate, receiveDate, isPaid, takeOut, discount)
VALUES (@custemerId, @employeeId, @orderDate, @receiveDate, @isPaid, @takeOut, @discount)
COMMIT TRANSACTION [Tran1]
END TRY
BEGIN CATCH
ROLLBACK TRANSACTION [Tran1]
END CATCH
END

CREATE PROCEDURE InsertIntoOrder @orderId INT,
@itemId INT,
@quantity INT
AS
BEGIN
IF (NOT EXISTS(SELECT orderId FROM Orders WHERE orderId = @orderId))
BEGIN
RAISERROR ('No such orderId', -1, -1)
RETURN
END
IF (NOT EXISTS(SELECT itemId FROM Dishes WHERE itemId = @itemId AND isActive = 1))
BEGIN
RAISERROR ('No such itemId or dish is not active', -1, -1)
RETURN
END
DECLARE @itemPrice INT
SET @itemPrice = (SELECT itemPrice
FROM Dishes
WHERE itemId = @itemId)
INSERT INTO OrderDetails(orderId, itemId, itemPrice, quantity)
VALUES (@orderId, @itemId, @itemPrice, @quantity)
END

CREATE PROCEDURE AddReservation @orderId INT,
@reservationDoneDate INT,
@reservationDate INT,
@numberOfGuests INT
AS
BEGIN
IF (NOT EXISTS (SELECT orderId FROM Orders WHERE orderId = @orderId))
BEGIN
RAISERROR ('No such orderId', -1, -1)
RETURN
END
IF (EXISTS (SELECT * FROM Orders WHERE orderId = @orderId AND isPaid = 1))
BEGIN
INSERT INTO Reservations(orderId, reservationDoneDate, reservationDate, numberOfGuests)
VALUES (@orderId, @reservationDoneDate, @reservationDate, @numberOfGuests)
END
ELSE
BEGIN
DECLARE @customerId INT
SET @customerId = (SELECT customerId from Orders where orderId = @orderId)
IF ((SELECT COUNT(*)
FROM Orders AS O
INNER JOIN OrderDetails AS OD
ON O.orderId = OD.orderID
WHERE O.customerId = @customerId
HAVING SUM((1 - O.discount) * OD.itemPrice * OD.quantity) > (SELECT WZ FROM Factors)) > (SELECT WK FROM Factors))
BEGIN
INSERT INTO Reservations(orderId, reservationDoneDate, reservationDate, numberOfGuests)
VALUES (@orderId, @reservationDoneDate, @reservationDate, @numberOfGuests)
END
ELSE
BEGIN
RAISERROR ('Client does not meet the requirements for reservation', -1, -1)
RETURN
END
END
END

CREATE PROCEDURE AddReservationDetails @reservationId INT,
@tableId INT,
@hourTimespan INT
AS
BEGIN
IF (NOT EXISTS(SELECT reservationId FROM Reservations WHERE reservationId = @reservationId))
BEGIN
RAISERROR ('No such reservationId', -1, -1)
RETURN
END
IF (NOT EXISTS(SELECT tableId FROM Tables WHERE tableId = @tableId))
BEGIN
RAISERROR ('No such tableId', -1, -1)
RETURN
END
DECLARE @reservationDate SMALLDATETIME
SET @reservationDate = (SELECT reservationDate FROM Reservations WHERE @reservationId =
reservationId)
IF (EXISTS(SELECT *
FROM Reservations AS R
INNER JOIN ReservationDetails AS RS ON RS.reservationId = R.reservationId
WHERE @tableId = tableId
AND DATEDIFF(HOUR, R.reservationDate, @reservationDate) < (@hourTimespan)))
BEGIN
RAISERROR ('Table occupied', -1, -1)
RETURN
END
INSERT INTO ReservationDetails(reservationId, tableId)
VALUES (@reservationId, @tableId)
END

CREATE PROCEDURE CreateInvoice @invoiceNumber INT,
@invoiceDate SMALLDATETIME,
@customerId INT,
@orderId INT
AS
BEGIN
IF (@invoiceDate > GETDATE())
BEGIN
RAISERROR ('Wrong date', -1, -1)
RETURN
END
IF (NOT EXISTS (SELECT customerId FROM Customers WHERE customerId = @customerId))
BEGIN
RAISERROR ('No such customerId', -1, -1)
RETURN
END
IF (NOT EXISTS (SELECT orderId FROM Orders WHERE orderId = @orderId))
BEGIN
RAISERROR ('No such orderId', -1, -1)
RETURN
END
DECLARE @address VARCHAR(100)
SET @address = (SELECT address FROM Customers WHERE customerId = @customerId)
DECLARE @city VARCHAR(100)
SET @city = (SELECT city FROM Customers WHERE customerId = @customerId)
DECLARE @postalCode VARCHAR(10)
SET @postalCode = (SELECT postalCode FROM Customers WHERE customerId = @customerId)
BEGIN TRANSACTION Tran2
BEGIN TRY
INSERT INTO Invoices(invoiceNumber, invoiceDate, customerId, address, city, postalCode)
VALUES(@invoiceNumber, @invoiceDate, @customerId, @address, @city, @postalCode)
DECLARE @biggestIndex INT
SET @biggestIndex = (SELECT TOP 1 invoiceId FROM Invoices ORDER BY invoiceId DESC) + 1
UPDATE Orders SET invoiceId = @biggestIndex WHERE orderId = @orderId
COMMIT TRANSACTION Tran2
END TRY
BEGIN CATCH
ROLLBACK TRANSACTION Tran2
END CATCH
END

CREATE PROCEDURE CreatePeriodicInvoice @invoiceNumber INT,
@invoiceDate SMALLDATETIME,
@customerId INT,
@month INT,
@year INT
AS
BEGIN
IF (@invoiceDate > GETDATE())
BEGIN
RAISERROR ('Wrong date', -1, -1)
RETURN
END
IF (NOT EXISTS (SELECT customerId FROM Customers WHERE customerId = @customerId))
BEGIN
RAISERROR ('No such customerId', -1, -1)
RETURN
END
DECLARE @address VARCHAR(100)
SET @address = (SELECT address FROM Customers WHERE customerId = @customerId)
DECLARE @city VARCHAR(100)
SET @city = (SELECT city FROM Customers WHERE customerId = @customerId)
DECLARE @postalCode VARCHAR(10)
SET @postalCode = (SELECT postalCode FROM Customers WHERE customerId = @customerId)
INSERT INTO Invoices(invoiceNumber, invoiceDate, customerId, address, city, postalCode)
VALUES(@invoiceNumber, @invoiceDate, @customerId, @address, @city, @postalCode)
DECLARE @biggestIndex INT
SET @biggestIndex = (SELECT TOP 1 invoiceId FROM Invoices ORDER BY invoiceId DESC) + 1
UPDATE Orders SET invoiceId = @biggestIndex WHERE invoiceId = NULL AND customerId = @customerId AND MONTH(orderDate) = @month AND YEAR(orderDate) = @year
BEGIN TRANSACTION Tran2
BEGIN TRY
INSERT INTO Invoices(invoiceNumber, invoiceDate, customerId, address, city, postalCode)
VALUES(@invoiceNumber, @invoiceDate, @customerId, @address, @city, @postalCode)
DECLARE @biggestIndex2 INT
SET @biggestIndex2 = (SELECT TOP 1 invoiceId FROM Invoices ORDER BY invoiceId DESC) + 1
UPDATE Orders SET invoiceId = @biggestIndex WHERE invoiceId = NULL
AND customerId = @customerId
AND MONTH(orderDate) = @month
AND YEAR(orderDate) = @year
COMMIT TRANSACTION Tran2
END TRY
BEGIN CATCH
ROLLBACK TRANSACTION Tran2
END CATCH
END

CREATE PROCEDURE ShowFreeTablesAt(@datetime AS smalldatetime, @timespan AS int)
AS
BEGIN
SELECT T.tableId
FROM Tables AS T
WHERE T.isActive = 1 AND T.tableId NOT IN (
SELECT T1.tableId
FROM Tables AS T1
INNER JOIN ReservationDetails AS RD
ON T1.tableId = RD.tableId
INNER JOIN Reservations AS R
ON RD.reservationId = R.reservationId
WHERE @datetime >= R.reservationDate AND @datetime <= DATEADD(MINUTE, @timespan, R.reservationDate))
END

CREATE PROCEDURE QualifiesForLifetimeDiscount(@customerId AS int)
AS
BEGIN
DECLARE @orderCount INT
SET @orderCount = (SELECT COUNT(*) FROM (
SELECT SUM(OD.itemPrice * OD.quantity  * (1-O.discount)) AS totalPrice
FROM OrderDetails AS OD
INNER JOIN Orders AS O
ON O.orderId = OD.orderId AND O.customerId = @customerId
GROUP BY O.OrderId
HAVING SUM(OD.itemPrice * OD.quantity  * (1-O.discount)) >= (SELECT K1 FROM Factors)) AS A)
IF(@orderCount >= (SELECT Z1 FROM Factors)
AND NOT EXISTS (
SELECT D.discountId FROM Discounts AS D
WHERE D.customerId = @customerId AND D.discountType = 'lifetime'
))
BEGIN
INSERT INTO Discounts values(@customerId, 'lifetime', GETDATE(), NULL)
END
END

CREATE PROCEDURE QualifiesForTemporaryDiscount(@customerId AS int)
AS
BEGIN
DECLARE @lastTemporaryDiscount SMALLDATETIME
SET @lastTemporaryDiscount = (
SELECT MAX(D.startDate)
FROM Discounts AS D
WHERE D.customerId = @customerId AND D.discountType = 'temporary'
)
DECLARE @totalCost MONEY
SET @totalCost = (
SELECT SUM(OD.itemPrice * OD.quantity  * (1-O.discount)) AS totalPrice
FROM OrderDetails AS OD
INNER JOIN Orders AS O
ON O.orderId = OD.orderId AND O.customerId = @customerId
WHERE O.orderDate > @lastTemporaryDiscount
GROUP BY O.OrderId
)
IF(@totalCost IS NULL OR @totalCost >= (SELECT K2 FROM Factors))
BEGIN
INSERT INTO Discounts values(@customerId, 'temporary', GETDATE(), 1)
END
END

CREATE PROCEDURE setOrderPaid(
@orderId INT)
AS
BEGIN
DECLARE @checkIsPaid BIT
SET @checkIsPaid = (SELECT isPaid FROM Orders O WHERE O.orderId = @orderId)
IF (@checkIsPaid = 0)
BEGIN
DECLARE @paid BIT
SET @paid = 1
UPDATE Orders
SET isPaid = @paid
END
ELSE
BEGIN
RAISERROR ('Order is already paid.', -1, -1)
END
END

CREATE PROCEDURE CancelOrder(@orderId AS int)
AS
BEGIN
IF (NOT EXISTS (SELECT orderId FROM Orders WHERE orderId = @orderId))
BEGIN
RAISERROR ('Order does not exists', -1, -1)
RETURN
END
IF ( NOT ((SELECT O.receiveDate FROM Orders AS O WHERE O.orderId = @orderId) < GETDATE()))
BEGIN
RAISERROR ('Order already completed', -1, -1)
RETURN
END
DELETE FROM Orders
WHERE Orders.orderId = @orderId
DELETE FROM OrderDetails
WHERE OrderDetails.orderId = @orderId
END

CREATE PROCEDURE CancelReservation(@reservationId AS int)
AS
BEGIN
IF (NOT EXISTS (SELECT reservationId FROM Reservations WHERE reservationId = @reservationId))
BEGIN
RAISERROR ('Reservation does not exists', -1, -1)
RETURN
END
IF ( NOT ((SELECT O.receiveDate FROM Orders AS O WHERE O.orderId = @reservationId) < GETDATE()))
BEGIN
RAISERROR ('Reservation already completed', -1, -1)
RETURN
END
DECLARE @orderId AS int
SET @orderId = (SELECT R.orderId FROM Reservations AS R WHERE R.reservationId = @reservationId)
EXEC CancelOrder @orderId
DELETE FROM Reservations
WHERE Reservations.reservationId = @reservationId
DELETE FROM ReservationDetails
WHERE ReservationDetails.reservationId = @reservationId
END

CREATE PROCEDURE ChangeFactors(
@WZ INT, @WK INT, @Z1 INT, @K1 INT, @R1 DECIMAL(3, 2), @K2 INT, @R2 DECIMAL(3, 2), @D1 INT)
AS
BEGIN
UPDATE Factors
SET WZ = @WZ
UPDATE Factors
SET WK = @WK
UPDATE Factors
SET Z1 = @Z1
UPDATE Factors
SET K1 = @K1
IF (@R1 BETWEEN 0.00 AND 1.00)
BEGIN
UPDATE Factors
SET R1 = @R1
END
ELSE
BEGIN
RAISERROR ('R1 factor is not between 0.00 and 1.00.', -1, -1)
END
UPDATE Factors
SET K2 = @K2
IF (@R2 BETWEEN 0.00 AND 1.00)
BEGIN
UPDATE Factors
SET R2 = @R2
END
ELSE
BEGIN
RAISERROR ('R2 factor is not between 0.00 and 1.00.', -1, -1)
END
UPDATE Factors
SET D1 = @D1
END

CREATE PROCEDURE ChangeCustomer(
@customerId INT,
@firstName VARCHAR(100),
@lastName VARCHAR(100),
@companyName VARCHAR(100) = NULL,
@phone VARCHAR(15),
@address VARCHAR(100) = NULL,
@city VARCHAR(100) = NULL,
@postalCode VARCHAR(100) = NULL,
@email VARCHAR(100) = NULL,
@takesPeriodicInvoice BIT)
AS
BEGIN
IF (NOT EXISTS(SELECT customerId FROM Customers WHERE customerId = @customerId))
BEGIN
RAISERROR ('No customer with such id', -1, -1)
END
ELSE
BEGIN
BEGIN TRANSACTION Tran2
BEGIN TRY
UPDATE Customers
SET firstName   = @firstName,
lastName    = @lastName,
companyName = @companyName,
phone       = @phone,
address     = @address,
city        = @city,
postalCode  = @postalCode
WHERE customerId = @customerId
IF (@email IS NULL OR @email LIKE '%_@%_.%_')
BEGIN
UPDATE Customers
SET email = @email
WHERE customerId = @customerId
END
ELSE
BEGIN
RAISERROR ('Email is not in email format.', -1, -1)
END
UPDATE Customers
SET takesPeriodicInvoice = @takesPeriodicInvoice
WHERE customerId = @customerId
COMMIT TRANSACTION Tran2
END TRY
BEGIN CATCH
ROLLBACK TRANSACTION Tran2
END CATCH
END
END

CREATE PROCEDURE ChangeEmployees(
@employeeId INT,
@firstName VARCHAR(100),
@lastName VARCHAR(100),
@birthDate SMALLDATETIME,
@hireDate SMALLDATETIME,
@position VARCHAR(100),
@phone VARCHAR(15),
@address VARCHAR(100),
@city VARCHAR(100),
@postalCode VARCHAR(10),
@reportsTo INT)
AS
BEGIN
IF (NOT EXISTS(SELECT @employeeId FROM Employees WHERE employeeId = @employeeId))
BEGIN
RAISERROR ('No employee with such id', -1, -1)
END
ELSE
BEGIN
BEGIN TRANSACTION Tran2
BEGIN TRY
UPDATE Employees
SET firstName  = @firstName,
lastName   = @lastName,
position = @position,
phone      = @phone,
address    = @address,
city       = @city,
postalCode = @postalCode,
reportsTo  = @reportsTo
WHERE @employeeId = employeeId
IF (@birthDate <= GETDATE())
BEGIN
UPDATE Employees
SET birthDate = @birthDate
WHERE @employeeId = employeeId
END
ELSE
BEGIN
RAISERROR ('Hire date is not before current date.', -1, -1)
END
IF (@hireDate <= GETDATE())
BEGIN
UPDATE Employees
SET hireDate = @hireDate
WHERE @employeeId = employeeId
END
ELSE
BEGIN
RAISERROR ('Hire date is not before current date.', -1, -1)
END
COMMIT TRANSACTION Tran2
END TRY
BEGIN CATCH
ROLLBACK TRANSACTION Tran2
END CATCH
END
END
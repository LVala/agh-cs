CREATE TRIGGER CheckOverlappingMenus
ON Menus
FOR INSERT AS
BEGIN
DECLARE @inDate SMALLDATETIME
SET @inDate = (SELECT inDate FROM inserted)
DECLARE @outDate SMALLDATETIME
SET @outDate = (SELECT outDate FROM inserted)
IF (EXISTS(SELECT *
FROM Menus
WHERE (@inDate < inDate AND inDate < @outDate AND @outDate < outDate)
OR (inDate < @inDate AND @inDate < outDate AND outDate < @outDate)
OR (inDate < @inDate AND @inDate < @outDate AND @outDate < outDate)
OR (@inDate < inDate AND inDate < outDate AND outDate < @outDate)))
BEGIN
RAISERROR ('Menus are overlapping.', -1, -1)
ROLLBACK TRANSACTION
END
END

CREATE TRIGGER DishesWithSeafood
ON OrderDetails
FOR INSERT, UPDATE
AS
BEGIN
IF ((SELECT C.CategoryName FROM Dishes AS D
INNER JOIN Categories AS C ON D.categoryId = C.categoryId
WHERE D.itemId = (SELECT itemId FROM INSERTED)) = 'Seafood')
BEGIN
DECLARE @receiveDate AS smalldatetime
SET @receiveDate = (SELECT O.receiveDate FROM Orders AS O WHERE O.orderId = (SELECT orderId FROM INSERTED))
IF (DATENAME(WEEKDAY, @receiveDate) NOT IN ('Thursday','Friday','Saturday'))
EGIN
RAISERROR ('Cannot order Seafood on that day of the week', -1, -1)
ROLLBACK TRANSACTION
RETURN
END
DECLARE @orderDate AS smalldatetime
SET @orderDate = (SELECT O.orderDate FROM Orders AS O WHERE O.orderId = (SELECT orderId FROM INSERTED))
IF (DATENAME(WEEKDAY, @receiveDate) = 'Thursday')
BEGIN
IF (@orderDate > DATEADD(DAY, -3, @receiveDate))
BEGIN
RAISERROR ('When ordering Seafood, must order before Monday of that week', -1, -1)
ROLLBACK TRANSACTION
RETURN
END
END
IF (DATENAME(WEEKDAY, @receiveDate) = 'Friday')
BEGIN
IF (@orderDate > DATEADD(DAY, -4, @receiveDate))
BEGIN
RAISERROR ('When ordering Seafood, must order before Monday of that week', -1, -1)
ROLLBACK TRANSACTION
RETURN
END
END
IF (DATENAME(WEEKDAY, @receiveDate) = 'Saturday')
BEGIN
IF (@orderDate > DATEADD(DAY, -5, @receiveDate))
BEGIN
RAISERROR ('When ordering Seafood, must order before Monday of that week', -1, -1)
ROLLBACK TRANSACTION
RETURN
END
END
END
END

CREATE TRIGGER OnlyOneFactors
ON Factors
FOR INSERT
AS
BEGIN
IF ((SELECT COUNT(*) FROM Factors) > 1)
BEGIN
RAISERROR ('No such reservationId', -1, -1)
ROLLBACK TRANSACTION
END
END

CREATE TRIGGER InvalidateMenuOnInsertion
ON MenuDetails
AFTER UPDATE, INSERT
AS
BEGIN
DECLARE @menuId AS INT
SET @menuId = (SELECT menuId FROM INSERTED)
UPDATE Menus SET isValid = 0 WHERE menuId = @menuId
END

CREATE TRIGGER OrderDateBeforeReceiveDate
ON Orders
FOR UPDATE, INSERT AS
BEGIN
DECLARE @orderDate AS SMALLDATETIME
SET @orderDate = (SELECT orderDate FROM INSERTED)
DECLARE @receiveDate AS SMALLDATETIME
SET @receiveDate = (SELECT receiveDate FROM INSERTED)
IF (@orderDate > @receiveDate)
BEGIN
RAISERROR('Order date cannot be higher than receiveDate.', -1, -1);
ROLLBACK TRANSACTION
RETURN
END
END
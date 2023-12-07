CREATE VIEW DishesFromLastTwoWeeks
AS
SELECT D.itemId, itemName
FROM Dishes as D
WHERE itemId IN (SELECT MD.itemId FROM MenuDetails AS MD
INNER JOIN Menus AS M ON M.MenuId = MD.MenuId
WHERE MD.menuId = M.menuId AND inDate < GETDATE() AND DATEDIFF(DAY, outDate, GETDATE()) < 14)

CREATE VIEW UpcomingReservations
AS
SELECT R.reservationId, R.numberOfGuests, R.reservationDate,
O.orderId, O.customerId, C.firstName, C.lastName,
SUM(OD.itemPrice * OD.quantity * (1-O.discount)) AS priceToPay
FROM dbo.Reservations AS R
INNER JOIN Orders AS O
ON R.orderId = O.orderId
INNER JOIN OrderDetails AS OD
ON O.orderId = OD.orderId
INNER JOIN Customers AS C
ON O.customerId = C.customerId
WHERE R.reservationDate >= GETDATE()
GROUP BY R.reservationId, R.numberOfGuests, R.reservationDate,
O.orderId, O.customerId, C.firstName, C.lastName

CREATE VIEW UpcomingOrders
AS SELECT O.orderId, O.receiveDate, O.takeOut,
O.isPaid, SUM(OD.itemPrice * OD.quantity * (1-O.discount)) AS OrderPrice,
C.customerId, C.firstName, C.lastName
FROM Orders AS O
INNER JOIN OrderDetails AS OD
ON O.orderId = OD.orderId
INNER JOIN Customers AS C
ON O.customerId = C.customerId
WHERE O.receiveDate >= GETDATE()
GROUP BY O.orderId, O.receiveDate, O.takeOut,
O.isPaid, C.customerId, C.firstName, C.lastName

CREATE VIEW GeneralOrdersStats AS
SELECT YEAR(O.orderDate) AS 'Order year',
MONTH(O.orderDate) AS 'Order month',
SUM(OD.quantity * OD.itemPrice * (1 - O.discount)) AS 'Total income',
AVG(OD.quantity * OD.itemPrice * (1 - O.discount)) AS 'Average order price',
SUM(OD.quantity * OD.itemPrice * O.discount) AS 'Price lost on discounts',
COUNT(O.orderId) AS 'Number of orders'
FROM dbo.Orders AS O
INNER JOIN dbo.OrderDetails OD ON O.orderId = OD.orderId
GROUP BY YEAR(O.orderDate), MONTH(O.orderDate)

CREATE VIEW TableReservationCount AS
SELECT T.tableId AS 'Table id',
YEAR(R.reservationDate) AS 'Reservation Year',
MONTH(R.reservationDate) AS 'Reservation Month',
COUNT(*) AS 'Number of reservations'
FROM Tables AS T
INNER JOIN ReservationDetails RD ON T.tableId = RD.tableId
INNER JOIN Reservations R ON R.reservationId = RD.reservationId
GROUP BY T.tableId, YEAR(R.reservationDate), MONTH(R.reservationDate)

CREATE VIEW DishPurchaseCount AS
SELECT itemName, YEAR(orderDate) AS year, MONTH(orderDate) AS month, COUNT(D.itemId) AS itemCount
FROM Dishes AS D
INNER JOIN OrderDetails AS OD ON D.itemId = OD.itemId
INNER JOIN Orders AS O ON O.orderId = OD.orderId
GROUP BY YEAR(orderDate), MONTH(orderDate), D.itemId, itemName

CREATE VIEW CustomerSpendingsStats AS
SELECT C.customerId, C.firstName, C.lastName, C.companyName,
SUM(OD.itemPrice * OD.quantity * (1 - O.discount)) AS totalSpendings
FROM Customers AS C
INNER JOIN Orders AS O
ON C.customerId = O.OrderId
INNER JOIN OrderDetails AS OD
ON O.orderId = OD.orderId
GROUP BY C.customerId, C.firstName, C.lastName, C.companyName
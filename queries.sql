drop database if exists FuelInventoryDB;
create database FuelInventoryDB;
USE FuelInventoryDB;

create table Categories
(categoryID int primary key,
categoryname varchar(50) notnull);

create table Items
(itemid int primary key,
itemname varchar(100) notnull,
categoryid int,
unit varchar(30),
sellingprice decimal(10,2),
FOREIGN KEY(categoryid)
REFERENCES Categories(categoryid));

create table Suppliers
(supplierid int primary key,
suppliername varchar(100),
phone varchar(20),
address varchar(200));

create table Stock
(itemid int primary key,
quantity decimal(12,2),
reorderlevel decimal(12,2),
FOREIGN KEY(itemid)
REFERENCES Items(itemid));

create table Purchases
(purchaseid int primary key,
supplierid int,
purchasedate date,
totalamount decimal(12,2),
FOREIGN KEY(supplierid)
REFERENCES Suppliers(supplierid));

create table PurchaseDetails
(purchasedetailid int primarykey,
purchsseid int,
itemid int,
quantity decimal(10,2),
rate decimal(10,2),
FOREIGN KEY(purchaseid)
REFERENCES Purchases(purchaseid),
FOREIGN KEY(itemid)
REFERENCES Items(itemid));

create table Sales
(saleid int primary key,
itemid int,
saledate date,
quantitysold decimal(12,2),
rate decimal(10,2)
totalamount decimal(12,2),
FOREIGN KEY(itemid)
REFERENCES Items(itemid));

create table DispenserReadings
(readingid int primary key,
itemid int,
readingdate date,
openingreading decimal(12,2),
closingreading decimal(12,2),
FOREIGN KEY(itemid)
REFERENCES Items(itemid));

show tables;

desc Categories;
desc Items;
desc Suppliers;
desc Stock;
desc Purchases;
desc PurchaseDetails;
desc Sales;
desc DispenserReadings;

insert into Categories values(1,'Fuel'),(2,'Lubricant');

insert into Items values
(1,'Petrol',1,'Litres',102.50),
(2,'Diesel',1,'Litres',90.20),
(3,'2T Oil',2,'Bottle',150.00),
(4,'Engine oil',2,'Bottle',550.00),
(5,'Premium petrol',1,'Litres',108.75),
(6,'Gear oil',2,'Bottle',320.00);

insert into Suppliers values
(1,'Indian oil cooperation','9876543210','Kochi'),
(2,'Bharat petroleum','9876501234','Thiruvananthapuram'),
(3,'Hindustan petroleum','998776655','Kozhikode'),
(4,'Reliance petroleum','9123456789','Ernakulam');

insert into Stock values
(1,5000.00,1000.00),
(2,3500.00,800.00),
(3,120.00,25.00),
(4,80.00,20.00),
(5,2000.00,500.00),
(6,60.00,15.00);

insert into Purchases values
(101,1,'2026-07-01',339300.00),
(102,2,'2026-07-04',233000.00),
(103,3,'2026-07-06',111000.00),
(104,4,'2026-07-08',120000.00);

insert into PurchaseDetails values
(1,101,2000,100.00),
(2,101,1500,92.00),
(3,102,300,140.00),
(4,102,200,525.00),
(5,103,1000,105,00),
(6,104,250,300.00);

insert into Sales values
(201,1,'2026-07-01',450,102.50,46125.00),
(202,2,'2026-07-01',300,90.20,27060.00),
(203,3,'2026-07-02',25,150.00,3750.00),
(204,4,'2026-07-03',15,550.00,8250.00),
(205,5,'2026-07-04',500,108.75,54375.00),
(206,6,'2026-07-05',30,320.00,9600.00),
(207,7,'2026-07-06',600,102.50,61500.00),
(208,2,'2026-07-06',400,90.20,36080.00);

insert into DispenserReadings values
(1,1,'2026-07-01',12000,12450),
(2,2,'2026-07-01',8500,8750),
(3,3,'2026-07-02',12450,12900),
(4,4,'2026-07-02',8750,9050),
(5,5,'2026-07-03',12900,13350),
(6,6,'2026-07-03',9050,9300),
(7,7,'2026-07-04',5000,5500),
(8,2,'2026-07-05',13350,13900);

select*from Categories;
select*from Items;
select*from Suppliers;
select*from Stock;
select*from Purchases;
select*from PurchaseDetails;
select*from Sales;
select*from DispenserReadings;

UPDATE Items
SET sellingprice = 103.00
WHERE itemid = 1;

UPDATE Suppliers
SET phone = '9999999999'
WHERE supplierid = 2;

UPDATE Stock
SET reorderlevel = 1000
WHERE itemid = 2;


UPDATE Stock
SET quantity = quantity + 2000
WHERE itemid = 1;

UPDATE Stock
SET quantity = quantity + 1500
WHERE itemid = 2;

UPDATE Stock
SET quantity = quantity + 300
WHERE itemid = 3;

UPDATE Stock
SET quantity = quantity + 200
WHERE itemid = 4;

UPDATE Stock
SET quantity = quantity + 1000
WHERE itemid = 5;

UPDATE Stock
SET quantity = quantity + 250
WHERE itemid = 6;


UPDATE Stock
SET quantity = quantity - 450
WHERE itemid = 1;

UPDATE Stock
SET quantity = quantity - 300
WHERE itemid = 2;

UPDATE Stock
SET quantity = quantity - 25
WHERE itemid = 3;

UPDATE Stock
SET quantity = quantity - 15
WHERE itemid = 4;

UPDATE Stock
SET quantity = quantity - 500
WHERE itemid = 5;

UPDATE Stock
SET quantity = quantity - 30
WHERE itemid = 6;

UPDATE Stock
SET quantity = quantity - 600
WHERE itemid = 1;

UPDATE Stock
SET quantity = quantity - 400
WHERE itemid = 2;


INSERT INTO Suppliers
VALUES
(5,'Test Supplier','9000000000','Temporary Address');

DELETE FROM Suppliers
WHERE supplierid = 5;

UPDATE Items
SET sellingprice = sellingprice + 2
WHERE categoryid = 1;

SELECT * FROM Items;

SELECT * FROM Suppliers;

SELECT * FROM Stock;

SELECT * FROM Sales;

SELECT * FROM Purchases;

SELECT
itemid,
quantity,
reorderlevel
FROM Stock;

SELECT
purchaseid,
itemid,
quantity,
rate,
(quantity*rate) AS PurchaseAmount
FROM PurchaseDetails;

select
saleid,
itemid,
quantitysold,
rate,
totalamount
FROM Sales;

SELECT * FROM Categories;
SELECT * FROM Items;
SELECT * FROM Suppliers;
SELECT * FROM Stock;
SELECT * FROM Purchases;
SELECT * FROM PurchaseDetails;
SELECT * FROM Sales;
SELECT * FROM DispenserReadings;



SELECT *
FROM Items
WHERE sellingprice > 100;

SELECT *
FROM Stock
WHERE quantity > 1000;

SELECT *
FROM Suppliers
WHERE address='Kochi';


SELECT *
FROM Items
ORDER BY sellingprice DESC;

SELECT *
FROM Suppliers
ORDER BY suppliername;


SELECT COUNT(*) AS TotalItems
FROM Items;

SELECT SUM(quantity)
AS TotalStock
FROM Stock;

SELECT AVG(sellingprice)
AS AveragePrice
FROM Items;

SELECT MAX(sellingprice)
AS HighestPrice
FROM Items;

SELECT MIN(sellingprice)
AS LowestPrice
FROM Items;


SELECT
categoryid,
COUNT(*) AS NumberOfItems
FROM Items
GROUP BY categoryid;

SELECT
itemid,
SUM(quantitysold) AS TotalQuantitySold
FROM Sales
GROUP BY itemid;


SELECT
I.itemname,
C.categoryname,
I.unit,
I.sellingprice
FROM Items I
INNER JOIN Categories C
ON I.categoryid=C.categoryid;


SELECT
P.purchaseid,
S.suppliername,
P.purchasedate,
P.totalamount
FROM Purchases P
INNER JOIN Suppliers S
ON P.supplierid=S.supplierid
ORDER BY P.purchasedate;


SELECT
PD.purchasedetailid,
I.itemname,
PD.quantity,
PD.rate,
(PD.quantity*PD.rate) AS Amount
FROM PurchaseDetails PD
INNER JOIN Items I
ON PD.itemid=I.itemid;


SELECT
S.saleid,
I.itemname,
S.saledate,
S.quantitysold,
S.rate,
S.totalamount
FROM Sales S
INNER JOIN Items I
ON S.itemid=I.itemid
ORDER BY S.saledate;


SELECT
I.itemname,
ST.quantity AS CurrentStock,
I.unit
FROM Items I
INNER JOIN Stock ST
ON I.itemid=ST.itemid;


SELECT
I.itemname,
ST.Qlquantity,
ST.reorderlevel
FROM Items I
INNER JOIN Stock ST
ON I.itemid=ST.itemid
WHERE ST.quantity<ST.reorderlevel;


SELECT
D.readingdate,
I.itemname,
D.openingreading,
D.closingreading,
(D.closingreading-D.openingreading)
AS FuelDispensed
FROM DispenserReadings D
INNER JOIN Items I
ON D.itemid=I.itemid
ORDER BY D.readingdate;


SELECT
I.itemname,
ST.quantity,
I.sellingprice,
(ST.quantity*I.sellingprice)
AS StockValue
FROM Items I
INNER JOIN Stock ST
ON I.itemid=ST.itemid;


SELECT
I.itemname,
SUM(S.quantitysold) AS QuantitySold,
SUM(S.totalamount) AS SalesAmount
FROM Sales S
INNER JOIN Items I
ON S.itemid=I.itemid
GROUP BY I.itemname;

SELECT
I.itemname,
SUM(PD.quantity) AS PurchasedQuantity
FROM PurchaseDetails PD
INNER JOIN Items I
ON PD.itemid=I.itemid
GROUP BY I.itemname;


SELECT
C.categoryname,
I.itemname
FROM Categories C
INNER JOIN Items I
ON C.categoryid=I.categoryid;


SELECT
I.itemname,
ST.quantity,
ST.reorderlevel
FROM Items I
INNER JOIN Stock ST
ON I.itemid=ST.itemid;


SELECT *
FROM Sales
WHERE totalamount>30000;


SELECT *
FROM Purchases
WHERE totalamount>100000;


SELECT
SUM(totalamount)
AS TotalRevenue
FROM Sales;


SELECT
SUM(totalamount)
AS TotalPurchaseCost
FROM Purchases;


SELECT
SUM(ClosingReading-OpeningReading)
AS TotalFuelDispensed
FROM DispenserReadings;



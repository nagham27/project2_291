# project2_291
Group Number: 92

CCID: Name<br />
eldegwy: Nagham Hesham Mohamed Hassan Eldegwy<br />
trotskay: Maria Trotskaya<br />
singarac: Yesith Singarachchige<br />


"We declare that we did not collaborate with anyone outside our own
group in this assignment"

Explanation:<br /><br />

Q1:<br />
SELECT COUNT( * ) <br />
FROM ( SELECT Orders.order_id<br />
       FROM Customers, Orders, Order_items<br />
       WHERE Customers.customer_postal_code = {randomCode}<br />
                AND Orders.order_id = Order_items.order_id<br />
                AND Orders.customer_id = Customers.customer_id  <br />
       GROUP BY (Orders.order_id)<br />
       HAVING COUNT( * ) > 1);<br />
       
No index was created for Orders.order_id beacuse order_id is a primary key and SQLite will automatically create an index on it.<br />
No index was created for Customers.customer_id beacuse customer_id is a primary key and SQLite will automatically create an index on it.<br />
No index was created for Order_items.order_id beacuse order_id is part of the primary key and SQLite will automatically create an index.<br />
The index  order_cid_index was created on the customer_id column of the Orders table due to the use of this statement "Orders.order_id = Order_items.order_id" in the WHERE clause. Creating this index makes look up faster.<br />
The index  customer_postal_index was created on the customer_postal_code column of the Customers table due to the use of this statement "Customers.customer_postal_code = {randomCode}" in the WHERE clause. Creating this index makes look up faster. randomCode is just a randomly generated postal code.<br /> <br />


Q2:
creates a view called "OrderSize" that counts the number of orders made by customers with a specific postal code. the variable "randomCode" has a value assigned to it by "SELECT customer_postal_code FROM Customers ORDER BY RANDOM() LIMIT 50" which retrieves the customer postal codes for 50 randomly selected customers from the "Customers" table.
The view can be queried using the SELECT statement:
SELECT * FROM [OrderSize];
This will return a single column with the count of orders made by customers with the specified postal code.
Lastly, the code includes a DROP VIEW statement, which is used to delete the view if it already exists in the database.

Q3:
calculates the number of orders made by customers with a specific postal code that have at least one order item with a quantity greater than average order item in another order. Here is a breakdown of the query:
SELECT COUNT(DISTINCT oi.order_id): calculates the count of distinct order IDs that satisfy the conditions in the WHERE clause.
FROM Customers c: specifies the "Customers" table as the starting point for the query.
JOIN Orders o ON c.customer_id = o.customer_id: joins the "Orders" table to the query based on the "customer_id" column.
JOIN Order_items oi ON o.order_id = oi.order_id: joins the "Order_items" table to the query based on the "order_id" column.
JOIN (SELECT order_id, COUNT(order_item_id) AS size FROM Order_items GROUP BY order_id) os ON oi.order_id = os.order_id: joins a subquery that calculates the number of order items per order and assigns the result to the alias "os". This subquery is used later to compare the size of order items in different orders.
WHERE c.customer_postal_code = {randomCode}: restricts the query to customers with a specific postal code.
AND oi.order_id IN (SELECT oi2.order_id FROM Order_items oi2 JOIN (SELECT order_id, COUNT(order_item_id) AS size FROM Order_items GROUP BY order_id) os2 ON oi2.order_id = os2.order_id WHERE os2.size > os.size GROUP BY oi2.order_id): restricts the query to orders where at least one order item has a quantity greater than the avg order item in any other order. This is done using a subquery that calculates the number of order items per order and compares them with the "os" subquery.

Q4:<br />
SELECT COUNT (DISTINCT Sellers.seller_postal_code)<br />
    FROM Customers , Orders , Sellers <br />
    WHERE Customers.customer_id = Orders.customer_id AND Customers.customer_id = <br />
    (SELECT customer_id <br />
    FROM Orders <br />
    GROUP BY customer_id <br />
    HAVING COUNT(*) > 1 <br />
    ORDER BY RANDOM() <br />
    LIMIT 1); <br />
    
No index was created for Customers.customer_id beacuse customer_id is a primary key and SQLite will automatically create an index on it.<br /> 
The index  customer_id_index was created on the customer_id column of the Orders table due to the use of this statement "Customers.customer_id = Orders.customer_id" in the WHERE clause. Creating this index makes look up faster.<br />




Reasons for User-optimization indexes
"Customers" table >> "customer_postal_code" index because Q1,and Q2 and Q3 queries filter or sort customers based on their postal code.
"Sellers" table >> "seller_postal_code" index since Q4 filter or sort sellers based on their postal code.
"orders" table >> "customer_id" since customer_id is the most frequently queried column in all queries.
 

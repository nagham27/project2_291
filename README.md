# project2_291
Group Number: 92

CCID: Name<br />
eldegwy: Nagham Hesham Mohamed Hassan Eldegwy<br />
trotskay: Maria Trotskaya<br />
singarac: Yesith Singarachchige<br />


"We declare that we did not collaborate with anyone outside our own
group in this assignment"


Q2:
creates a view called "OrderSize" that counts the number of orders made by customers with a specific postal code. the variable "randomCode" has a value assigned to it by "SELECT customer_postal_code FROM Customers ORDER BY RANDOM() LIMIT 50" which retrieves the customer postal codes for 50 randomly selected customers from the "Customers" table.
The view can be queried using the SELECT statement:
SELECT * FROM [OrderSize];
This will return a single column with the count of orders made by customers with the specified postal code.
Lastly, the code includes a DROP VIEW statement, which is used to delete the view if it already exists in the database.

Q3:

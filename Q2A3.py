import numpy as np
import sqlite3
import time
import matplotlib.pyplot as plt

dbCursor = None
connection = None
uninformedResults = [] 
selfResults = [] 
userResults = []


def initialize(dbName):
    global dbCursor, connection
    connection = sqlite3.connect(dbName)
    dbCursor = connection.cursor()
    # enable use of forgein (by default, SQLite does not enforce foreign keys)
    dbCursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()

def uninformed():
    #turn off auto indexing
    dbCursor.execute('PRAGMA automatic_index = FALSE;')
    
    script = '''
    CREATE TABLE SecondCustomers (
    customer_id TEXT,
    customer_postal_code INTEGER
    );
    INSERT INTO SecondCustomers SELECT customer_id, customer_postal_code FROM Customers;
    
    CREATE TABLE SecondSellers (
        seller_id TEXT,
        seller_postal_code INTEGER
    );
    INSERT INTO SecondSellers SELECT seller_id, seller_postal_code FROM Sellers;
    CREATE TABLE SecondOrders (
        order_id TEXT,
        customer_id TEXT
    );
    INSERT INTO SecondOrders SELECT order_id, customer_id FROM Orders;
    CREATE TABLE SecondOrder_items (
        order_id TEXT,
        order_item_id INTEGER,
        product_id TEXT,
        seller_id TEXT
    );
    INSERT INTO SecondOrder_items SELECT order_id, order_item_id, product_id, seller_id FROM Order_items;
    ALTER TABLE Order_items RENAME TO FirstOrder_items;
    ALTER TABLE SecondOrder_items RENAME TO Order_items;
    
    ALTER TABLE Orders RENAME TO FirstOrders;
    ALTER TABLE SecondOrders RENAME TO Orders;
    
    ALTER TABLE Sellers RENAME TO FirstSellers;
    ALTER TABLE SecondSellers RENAME TO Sellers;
    
    ALTER TABLE Customers RENAME TO FirstCustomers;
    ALTER TABLE SecondCustomers RENAME TO Customers;
    '''

    dbCursor.executescript(script)

def selfOptimized():
    # enable auto indexing
    dbCursor.execute('PRAGMA automatic_index = True')

    script = '''
    
    DROP TABLE Customers;
    DROP TABLE Sellers;
    DROP TABLE Orders;
    DROP TABLE Order_items;
    ALTER TABLE FirstCustomers RENAME TO Customers;
    ALTER TABLE FirstSellers RENAME TO Sellers;
    ALTER TABLE FirstOrders RENAME TO Orders;
    ALTER TABLE FirstOrder_items RENAME TO Order_items;
    
    '''
    dbCursor.executescript(script)

def userOptimized():
    dbCursor.execute('PRAGMA automatic_index = true;')
    dbCursor.execute('CREATE INDEX customer_postal_index ON Customers(customer_postal_code);')
    dbCursor.execute('CREATE INDEX order_cid_index ON Orders(customer_id);')
    dbCursor.execute('CREATE INDEX seller_postal_code_idx ON Sellers(seller_postal_code);')
    dbCursor.execute('CREATE INDEX order_items_product_id_idx ON Order_items(product_id);')

def solveQuery(randomCode):
    script = f'''

    CREATE VIEW [OrderSize] AS SELECT COUNT(order_id) FROM Customers c, Orders o WHERE c.customer_id = o.customer_id AND customer_postal_code = {randomCode};


    SELECT * FROM [OrderSize];

    DROP VIEW IF EXISTS OrderSize;


    '''
    dbCursor.executescript(script)

def runSolveQuery():
    
    # get random codes
    dbCursor.execute('SELECT customer_postal_code FROM Customers ORDER BY RANDOM() LIMIT 50')
    randomCodes = dbCursor.fetchall()
    totalTime = 0
    for i in range(50):
        startTime = time.time()
        solveQuery(randomCodes[i][0])
        endTime = time.time()
        runTime = (endTime - startTime)*1000
        totalTime += runTime
    
    return totalTime/50

def dropIndices():
    dbCursor.execute('DROP INDEX customer_postal_index')
    dbCursor.execute('DROP INDEX order_cid_index')
    dbCursor.execute('DROP INDEX seller_postal_code_idx')
    dbCursor.execute('DROP INDEX order_items_product_id_idx')



def collectResults():
    global connection, dbCursor

    uninformed()
    query1 = runSolveQuery()
    uninformedResults.append(query1)

    selfOptimized()
    query2 = runSolveQuery()
    selfResults.append(query2)

    userOptimized()
    query3 = runSolveQuery()
    userResults.append(query3)
    
    dropIndices()
    connection.commit()

def drawGraph(uninformedPlot, selfPlot, userPlot):
    width = 0.6
    dbLabels = ['SmallDB', 'MediumDB', 'LargeDB']

    _, axes = plt.subplots()
    #add data 
    #need to increment bottom offset for each type of optimization
    axes.bar(dbLabels, uninformedPlot, width, label = 'Uninformed')
    axes.bar(dbLabels, selfPlot, width, bottom = uninformedPlot, label = 'Self-Optimized')
    axes.bar(dbLabels, userPlot, width, bottom = np.array(uninformedPlot) + np.array(selfPlot), label='User-Optimized')

    axes.set_title('Q2 (Runtime in ms)')
    axes.legend()

    plt.savefig('./Q3A2chart.png')
    print('Chart saved to file')
    
    plt.close()

def solveQuestion2():
    global connection, cursor
    dbNames = ["./A3Small.db", "./A3Medium.db", "./A3Large.db"]
    
    for i in range(len(dbNames)):
        initialize(dbNames[i])
        print("Connected to DB: ", dbNames[i])
        collectResults()
        connection.commit()
        connection.close()
        print("Connection closed!")
    drawGraph(uninformedResults, selfResults, userResults)

if __name__ == "__main__":
    solveQuestion2()
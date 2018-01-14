import psycopg2


def create_products(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS products''')
    cursor.execute('''CREATE TABLE products
                     ("ID" INT PRIMARY KEY NOT NULL,
                      "Name" TEXT NOT NULL,
                      "Quantity" INT NULL,
                      "Selling price" FLOAT NOT NULL,
                      "Category" CHAR(3) NOT NULL);''')
    connection.commit()
    for row in data:
        sql = "INSERT INTO products VALUES (%s, %s, %s, %s, %s)"
        data = row
        cursor.execute(sql, data)
        connection.commit()
    connection.close()


data = ((1, 'Samsung S8/32GB/Black', 4, 2900, "MOB"), (2, 'LG G6/32GB/Grey', 12, 2300, "MOB"),
        (3, 'Fifa18 PC', 32, 219, "GAM"))
#create_products(data)


def create_ordered_products(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS ordered_position''')
    cursor.execute('''CREATE TABLE ordered_position
                     ("ID" SERIAL NOT NULL,
                      "Quantity" INT NOT NULL,
                      "ID_prod" INT NOT NULL,
                      "ID_ord" INT NOT NULL
                      CONSTRAINT fk_prod
                      FOREIGN KEY ("ID_prod")
                      REFERENCES products ("ID")
                      CONSTRAINT fk_ord
                      FOREIGN KEY ("ID_ord")
                      REFERENCES orders ("ID"));''')
    connection.commit()
    for row in data:
        sql = "INSERT INTO ordered_position VALUES (%s, %s, %s)"
        data = row
        cursor.execute(sql, data)
        connection.commit()
    connection.close()


#data_pos = ((1, 1, 1), (2, 2, 2), (3, 3, 3))
#create_ordered_products(data_pos)


def create_orders(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS orders''')
    cursor.execute('''CREATE TABLE orders
                     ("ID" SERIAL NOT NULL,
                      "Order date" DATE,
                      "Order time" TIME);;''')
    connection.commit()
    for row in data:
        sql = "INSERT INTO orders VALUES (%s, %s, %s)"
        data = row
        cursor.execute(sql, data)
        connection.commit()
    connection.close()


# data_ord = ((1, '2017-11-28 11:45:45', '2017-12-03 10:56:11'), (2, '2017-11-28 12:12:56', '2017-12-03 14:14:45'))
# create_orders(data_ord)

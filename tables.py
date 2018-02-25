import psycopg2


def create_products(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DROP TABLE IF EXISTS products CASCADE'''
    cursor.execute(sql)

    sql = '''
    CREATE TABLE products
    (
        "ID"            SERIAL PRIMARY KEY NOT NULL,
        "Name"          TEXT               NOT NULL,
        "Quantity"      INT                NULL,
        "Selling price" FLOAT              NOT NULL,
        "Category"      CHAR(3)            NOT NULL
    )
    '''
    cursor.execute(sql)
    connection.commit()

    sql = '''
    INSERT INTO products
    ("Name", "Quantity", "Selling price", "Category")
    VALUES (%s, %s, %s, %s)
    '''
    for row in data:
        cursor.execute(sql, row)

    connection.commit()
    connection.close()


data = (('Samsung S8/32GB/Black', 4, 2900, "MOB"), ('LG G6/32GB/Grey', 12, 2300, "MOB"), ('Fifa18 PC', 32, 219, "GAM"),
        ('Nokia Lumia 900', 12, 700, "MOB"),)


def create_orders(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DROP TABLE IF EXISTS orders CASCADE'''
    cursor.execute(sql)

    sql = '''
    CREATE TABLE orders
    (
        "ID"           SERIAL PRIMARY KEY NOT NULL,
        "Order Date"   TIMESTAMP          NOT NULL,
        "Payment Date" TIMESTAMP          NULL,
        "ID_cust"      INT                NOT NULL REFERENCES customers ("ID")
    )
    '''
    cursor.execute(sql)
    connection.commit()

    sql = '''
    INSERT INTO orders
    ("Order Date", "Payment Date", "ID_cust")
    VALUES (%s, %s, %s)
    '''
    for row in data:
        cursor.execute(sql, row)

    connection.commit()
    connection.close()


data_ord = (('2017-11-28 11:45:45', '2017-11-29 12:45:45', 1), ('2017-11-28 12:12:56', '2017-11-30 21:12:56', 2))


def create_ordered_products(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DROP TABLE IF EXISTS ordered_position CASCADE'''
    cursor.execute(sql)

    sql = '''
    CREATE TABLE ordered_position
    (
        "ID"            SERIAL PRIMARY KEY NOT NULL,
        "Quantity"      INT                NOT NULL,
        "Selling price" FLOAT              NOT NULL,
        "ID_prod"       INT                NOT NULL REFERENCES products ("ID"),
        "ID_ord"        INT                NOT NULL REFERENCES orders ("ID")
    )
    '''
    cursor.execute(sql)
    connection.commit()

    sql = '''
    INSERT INTO ordered_position
    ("Quantity", "Selling price", "ID_prod", "ID_ord")
    VALUES (%s, %s, %s, %s)
    '''
    for row in data:
        cursor.execute(sql, row)

    connection.commit()
    connection.close()


data_pos = ((1, 2900, 1, 1), (2, 219, 3, 2), (5, 2900, 1, 2), (7, 700, 4, 2), (2, 2300, 2, 1))


def create_customers(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DROP TABLE IF EXISTS customers CASCADE'''
    cursor.execute(sql)

    sql = '''
    CREATE TABLE customers
    (
        "ID"           SERIAL PRIMARY KEY,
        "Name"         TEXT,
        "City"         TEXT,
        "Street"       TEXT,
        "House number" TEXT,
        "Zip code"     CHAR(6)
    )
    '''
    cursor.execute(sql)
    connection.commit()

    sql = '''
    INSERT INTO customers
    ("Name", "City", "Street", "House number", "Zip code")
    VALUES (%s, %s, %s, %s, %s)
    '''
    for row in data:
        cursor.execute(sql, row)

    connection.commit()
    connection.close()


data_customers = (
    ("Jan Kowalski", "Bydgoszcz", "Kwiatowa", "13A", "67-232"), ("Adam Nowak", "Katowice", "Mariacka", "2/5", "25-200"))


def create_vendors(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DROP TABLE IF EXISTS vendors CASCADE'''
    cursor.execute(sql)

    sql = '''
    CREATE TABLE vendors
    (
        "ID"           SERIAL PRIMARY KEY,
        "Name"         TEXT,
        "City"         TEXT,
        "Street"       TEXT,
        "House number" TEXT,
        "Zip code"     CHAR(6)
    )
    '''
    cursor.execute(sql)
    connection.commit()

    sql = '''
    INSERT INTO vendors
    ("Name", "City", "Street", "House number", "Zip code")
    VALUES (%s, %s, %s, %s, %s)
    '''
    for row in data:
        cursor.execute(sql, row)

    connection.commit()
    connection.close()


data_vendors = (("Frapol", "Szczecin", "Ogrodowa", "143", "78-456"), ("Rinus", "Rybnik", "Centralna", "2C", "41-328"))


def create_temp():
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''DROP TABLE IF EXISTS temp CASCADE'''
    cursor.execute(sql)

    sql = '''
    CREATE TABLE temp
    (
        "ID"            SERIAL PRIMARY KEY NOT NULL,
        "Item ID"       INT                NOT NULL,
        "Name"          TEXT,
        "Quantity"      INT                NOT NULL,
        "Selling Price" FLOAT              NOT NULL,
        "Category"      CHAR(3)
    )
    '''
    cursor.execute(sql)

    connection.commit()
    connection.close()


def fill_in_with_sample_data():
    create_products(data)
    create_vendors(data_vendors)
    create_customers(data_customers)
    create_orders(data_ord)
    create_ordered_products(data_pos)

#fill_in_with_sample_data()

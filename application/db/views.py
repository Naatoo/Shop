import psycopg2


def create_view_orders():
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    DROP VIEW IF EXISTS orders_view
    '''
    cursor.execute(sql)

    sql = '''
    CREATE VIEW orders_view AS
        SELECT
            "ID",
            (SELECT "Name"
             FROM
                 customers
             WHERE
                 orders."ID_cust" = customers."ID")       AS "Customer",
            "Order Date",
            "Payment Date",
            (SELECT SUM("Quantity" * "Selling price")
             FROM
                 ordered_position
             WHERE
                 ordered_position."ID_ord" = orders."ID") AS "Full price"
        FROM
            orders
    '''
    cursor.execute(sql)

    connection.commit()
    connection.close()


def create_view_orders_items(id_order):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    DROP VIEW IF EXISTS orders_items_view
    '''
    cursor.execute(sql)

    sql = '''
    CREATE VIEW orders_items_view AS
        SELECT
            products."ID",
            products."Name",
            (SELECT ordered_position."Quantity"
             WHERE
                 ordered_position."ID_prod" = products."ID") AS "Quantity",
            (SELECT ordered_position."Selling price"
             WHERE
                 ordered_position."ID_prod" = products."ID") AS "Selling price",
            (SELECT ordered_position."Quantity"
             WHERE
                 ordered_position."ID_prod" = products."ID") * (SELECT ordered_position."Selling price"
                                                                WHERE
                                                                    ordered_position."ID_prod" = products."ID")
                                                             AS "Total price",
            products."Category"
        FROM
            products, ordered_position
        WHERE
            products."ID" = ordered_position."ID_prod"
            AND
            ordered_position."ID_ord" = %s
        ORDER BY "Total price" DESC
    '''
    cursor.execute(sql, id_order)

    connection.commit()
    connection.close()

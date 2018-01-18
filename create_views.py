import psycopg2


def create_view_orders():
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP VIEW IF EXISTS orders_view''')
    cursor.execute('''CREATE VIEW orders_view AS
                    SELECT 
                        "ID",
                        "Order date",
                        "Order time",
                        (SELECT 
                                SUM("Quantity" * (SELECT 
                                            "Selling price"
                                        FROM
                                            products
                                        WHERE
                                            products."ID" = ordered_position."ID_prod"))
                            FROM
                                ordered_position
                            WHERE
                                orders."ID" = ordered_position."ID") AS "Full price"
                    FROM
                        orders;''')
    connection.commit()
    connection.close()


create_view_orders()

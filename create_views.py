import psycopg2


def create_view_orders():
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP VIEW IF EXISTS orders_view''')
    cursor.execute('''CREATE VIEW orders_view AS
                    SELECT 
                        "ID",
                        "Ordered",
                        "Paid",
                        (SELECT 
                                SUM("Quantity" * (SELECT 
                                            "Selling price"
                                        FROM
                                            products
                                        WHERE
                                            ordered_position."ID_prod" = products."ID"))
                            FROM
                                ordered_position
                            WHERE
                                ordered_position."ID_ord" = orders."ID") AS "Full price"     
                    FROM
                        orders
                    ''')
    connection.commit()
    connection.close()
create_view_orders()

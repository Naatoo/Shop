import psycopg2


def create_view_orders():
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP VIEW IF EXISTS orders_view''')
    cursor.execute('''CREATE VIEW orders_view AS
                    SELECT 
                        "ID",
                        (SELECT 
                                "Name"
                                FROM
                                    customers 
                                WHERE
                                    orders."ID_cust" = customers."ID") AS "Customer",
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


def create_view_orders_items(id_order):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP VIEW IF EXISTS orders_items_view''')
    sql = '''CREATE VIEW orders_items_view AS
                    SELECT 
                        products."ID",
                        products."Name",
                        (SELECT 
                                ordered_position."Quantity"
                                WHERE 
                                    ordered_position."ID_prod" = products."ID") AS "Quantity",
                        products."Selling price",
                        (SELECT 
                                ordered_position."Quantity"
                                WHERE 
                                    ordered_position."ID_prod" = products."ID") * products."Selling price" 
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



import psycopg2


def view(table_name):
    data = (table_name,)
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = "SELECT * FROM %s" % table_name
    cursor.execute(sql)
    rows = cursor.fetchall()

    sql = "SELECT column_name FROM information_schema.columns WHERE table_name=%s"
    cursor.execute(sql, data)
    column_names = cursor.fetchall()
    column_names_final = [tup[0] for tup in column_names]

    connection.close()
    return column_names_final, rows

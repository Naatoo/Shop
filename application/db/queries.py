import psycopg2


def view_data(table_name):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    SELECT *
    FROM %s ORDER BY "ID"
    ''' % table_name
    cursor.execute(sql)

    rows = cursor.fetchall()

    connection.close()
    return rows


def view_column_names(table_name):
    data = (table_name,)
    connection = psycopg2.connect("dbname='shop' user='postgres' password='postgres' host='localhost' port='5432'")
    cursor = connection.cursor()

    sql = '''
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = %s
    '''
    cursor.execute(sql, data)

    column_names = cursor.fetchall()
    column_names_final = [tup[0].title() for tup in column_names]

    connection.close()
    return column_names_final

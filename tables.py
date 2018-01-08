import psycopg2


def create_table(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS products''')
    cursor.execute('''CREATE TABLE products
                   (Pozycja_towaru INT PRIMARY KEY NOT NULL,
                     Nazwa CHAR(40) NOT NULL,
                     Ilość_w_magazynie INT NULL,
                     Cena_sprzedaży FLOAT NOT NULL,
                     kat CHAR(3) NOT NULL);''')
    # INDEX `fk_kat_idx` (`id_kat` ASC),\
    # INDEX `fk_mag_idx` (`id_mag` ASC),\
    # CONSTRAINT `fk_kat`\
    #   FOREIGN KEY (`id_kat`)\
    #   REFERENCES `sklep_internetowy`.`Kategorie` (`Id_kat`)\
    # CONSTRAINT `fk_mag`\
    #   FOREIGN KEY (`id_mag`)\
    #   REFERENCES `sklep_internetowy`.`Magazyn` (`id_Magazynu`)"
    connection.commit()
    for row in data:
        sql = "INSERT INTO products VALUES (%s, %s, %s, %s, %s)"
        data = row
        cursor.execute(sql, data)
        connection.commit()
    connection.close()


def sql_insert(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = "INSERT INTO products VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    connection.commit()
    connection.close()

#
# def view():
#     connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM store")
#     rows = cursor.fetchall()
#     connection.close()
#     print(rows)
#     return rows
#
#

def delete(id):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    sql = "DELETE FROM products WHERE Pozycja_towaru=%s;"
    cursor.execute(sql, (id,))
    connection.commit()
    connection.close()


#
# def update(quantity, price, item):
#     connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
#     cursor = connection.cursor()
#     cursor.execute("UPDATE store SET quantity=%s, price=%s WHERE item=%s", (quantity, price, item))
#     connection.commit()
#     connection.close()


data = ((1, 'Telefon_Samsung_S8', 4, 2900, "MOB"), (2, 'Telefon LG G6/32GB/Szary', 12, 2300, "MOB"),
        (3, 'Gra Fifa18', 32, 219, "GAM"))


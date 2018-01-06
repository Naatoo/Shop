import psycopg2


def create_table(data):
    connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS products''')
    cursor.execute('''CREATE TABLE products
                   (Pozycja_towaru INT PRIMARY KEY NOT NULL,
                     Nazwa CHAR(70) NOT NULL,
                     Ilość_w_magazynie INT NULL,
                     Cena_sprzedaży FLOAT NOT NULL,
                     id_kat INT NOT NULL,
                     id_mag INT NOT NULL);''')
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
        sql = "INSERT INTO products VALUES (%s, %s, %s, %s, %s, %s)"
        data = row
        cursor.execute(sql, data)
        connection.commit()
    connection.close()


# def insert(item, quantity, price):
#     connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
#     cursor = connection.cursor()
#     # cursor.execute("INSERT INTO store VALUES ('%s','%s','%s')" % (item, quantity, price))
#     cursor.execute("INSERT INTO store VALUES (%s,%s,%s)",  (item, quantity, price))
#     connection.commit()
#     connection.close()
#
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
# def delete(item):
#     connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
#     cursor = connection.cursor()
#     cursor.execute("DELETE FROM store WHERE item=%s", (item,))
#     connection.commit()
#     connection.close()
#
#
# def update(quantity, price, item):
#     connection = psycopg2.connect("dbname='shop' user='postgres' password='natoo123' host='localhost' port='5432'")
#     cursor = connection.cursor()
#     cursor.execute("UPDATE store SET quantity=%s, price=%s WHERE item=%s", (quantity, price, item))
#     connection.commit()
#     connection.close()


data = ((1, 'Telefon_Samsung_S8', 4, 2900, 1, 1), (2, 'Telefon LG G6/32GB/Szary', 12, 2300, 1, 1),
        (3, 'Gra Fifa18', 32, 219, 2, 2))
create_table(data)


import csv
import psycopg2
import psycopg2.extras
import datetime

conn = None
cursor = None

try:
    t0 = datetime.datetime.now()
    conn = psycopg2.connect(
        database="test", user='postgres', password='password', host='127.0.0.1', port='5432'
    )

    cursor = conn.cursor()


    cursor.execute("DROP TABLE IF EXISTS PRODUCTS")

    productsql = """CREATE TABLE PRODUCTS(
                Product_Id SERIAL PRIMARY KEY NOT NULL,
                Campus VARCHAR DEFAULT 'hr-rfe',
                Name VARCHAR NOT NULL,
                Slogan VARCHAR NOT NULL,
                Description VARCHAR NOT NULL,
                Category VARCHAR NOT NULL,
                Default_Price int NOT NULL,
                Created_at timestamp DEFAULT CURRENT_TIMESTAMP,
                Updated_at timestamp DEFAULT CURRENT_TIMESTAMP
    )"""

    cursor.execute(productsql)
    with open("/home/andrewsittner/SDCCSVS/product.csv", 'r') as file:
        csvreader = csv.reader(file)
        count = 0
        values = []
        product_insert_script = 'INSERT INTO PRODUCTS (Product_Id, Name, Slogan, Description, Category, Default_Price) VALUES (%s, %s, %s, %s, %s, %s);'
        for row in csvreader:
            if count > 0:
                if len(row) != 6: 
                    print(row)
                values.append((row[0], row[1], row[2], row[3], row[4], row[5]))
            count = 1
            if len(values) == 1000:
                psycopg2.extras.execute_batch(cursor, product_insert_script, values, page_size=1000)
                del(values)
                values = []
        if len(values) > 0:
            psycopg2.extras.execute_batch(cursor, product_insert_script, values, page_size=1000)
            del(values)
            values = []
    cursor.execute("CREATE INDEX Product_Index ON PRODUCTS (Product_Id);")

    conn.commit()
    t1 = datetime.datetime.now()-t0
    print(t1, "Product Table created successfully........")

    cursor.execute("DROP TABLE IF EXISTS STYLES")

    stylessql = """CREATE TABLE STYLES(
                Style_Id SERIAL PRIMARY KEY NOT NULL,
                Product_Id INT NOT NULL, 
                Name VARCHAR NOT NULL,
                Original_Price VARCHAR,
                Sale_Price VARCHAR,
                Default_Int INT NOT NULL
    )"""

    cursor.execute(stylessql)

    with open("/home/andrewsittner/SDCCSVS/styles.csv", 'r') as file:
        csvreader = csv.reader(file)
        count = 0
        values = []
        Styles_insert_script = 'INSERT INTO STYLES (Style_Id, Product_Id, Name, Original_Price, Sale_Price, Default_Int) VALUES (%s, %s, %s, %s, %s, %s);'
        for row in csvreader:
            if count > 0:
                values.append((row[0], row[1], row[2], row[3], row[4], row[5]))
            count = 1
            if len(values) == 1000:
                psycopg2.extras.execute_batch(cursor, Styles_insert_script, values, page_size=1000)
                del(values)
                values = []
        if len(values) > 0:
            psycopg2.extras.execute_batch(cursor, Styles_insert_script, values, page_size=1000)
            del(values)
            values = []
    conn.commit()
    t1 = datetime.datetime.now()-t0
    cursor.execute("CREATE INDEX Style_Index ON STYLES (product_id);")
    print(t1, "Styles Table created successfully........")

    cursor.execute("DROP TABLE IF EXISTS FEATURES")

    featuressql = """CREATE TABLE FEATURES(
                Feature_Id SERIAL PRIMARY KEY NOT NULL,
                Product_Id INT NOT NULL,
                Feature VARCHAR NOT NULL,
                Value VARCHAR NOT NULL
    )"""

    cursor.execute(featuressql)

    with open("/home/andrewsittner/SDCCSVS/features.csv", 'r') as file:
        csvreader = csv.reader(file)
        Features_insert_script = 'INSERT INTO FEATURES (Feature_Id, Product_Id, Feature, Value) VALUES (%s, %s, %s, %s);'
        count = 0
        values = []
        for row in csvreader:
            if count > 0:
                values.append((row[0], row[1], row[2], row[3]))
            count = 1
            if len(values) == 1000:
                psycopg2.extras.execute_batch(cursor, Features_insert_script, values, page_size=1000)
                del(values)
                values = []
        if len(values) > 0:
            psycopg2.extras.execute_batch(cursor, Features_insert_script, values, page_size=1000)
            del(values)
            values = []
    t1 = datetime.datetime.now()-t0
    cursor.execute("CREATE INDEX Feature_Index ON FEATURES (product_id);")
    print(t1, "Features Table created successfully........")

    conn.commit()

    cursor.execute("DROP TABLE IF EXISTS SKUS")

    skussql = """CREATE TABLE SKUS(
                Skus_Id SERIAL PRIMARY KEY NOT NULL,
                Style_Id INT NOT NULL,
                Size VARCHAR NOT NULL,
                Quantity VARCHAR NOT NULL
    )"""

    cursor.execute(skussql)

    with open("/home/andrewsittner/SDCCSVS/skus.csv", 'r') as file:
        csvreader = csv.reader(file)
        Skus_insert_script = 'INSERT INTO SKUS (Skus_Id, Style_Id, Size, Quantity) VALUES (%s, %s, %s, %s);'
        values = []
        count = 0
        for row in csvreader:
            if count > 0:
                values.append((row[0], row[1], row[2], row[3]))
            count = 1
            if len(values) == 1000:
                psycopg2.extras.execute_batch(cursor, Skus_insert_script, values, page_size=1000)
                del(values)
                values = []
        if len(values) > 0:
            psycopg2.extras.execute_batch(cursor, Skus_insert_script, values, page_size=1000)
            del(values)
            values = []
    t1 = datetime.datetime.now()-t0
    cursor.execute("CREATE INDEX Skus_Index ON Skus (Style_Id);")
    print(t1, "Skus Table created successfully........")

    conn.commit()

    cursor.execute("DROP TABLE IF EXISTS PHOTOS")

    photossql = """CREATE TABLE PHOTOS(
                Photo_Id SERIAL PRIMARY KEY NOT NULL,
                Style_Id INT NOT NULL,
                Thumbnail_url VARCHAR NOT NULL,
                Url VARCHAR NOT NULL
    )"""

    cursor.execute(photossql)


    with open("/home/andrewsittner/SDCCSVS/photos.csv", 'r') as file:
        Photos_insert_script = 'INSERT INTO PHOTOS (Photo_Id, Style_Id, Thumbnail_url, Url) VALUES (%s, %s, %s, %s);'
        csvreader = csv.reader(file)
        values = []
        count = 0
        for row in csvreader:
            if count > 0: 
                if len(row) != 4:
                    print(row)
                values.append((row[0], row[1], row[2], row[3]))
            count = 1
            if len(values) == 1000:
                psycopg2.extras.execute_batch(cursor, Photos_insert_script, values, page_size=1000)
                del(values)
                values = []
        if len(values) > 0:
            psycopg2.extras.execute_batch(cursor, Photos_insert_script, values, page_size=1000)
            del(values)
            values = []
    t1 = datetime.datetime.now()-t0
    cursor.execute("CREATE INDEX Photos_Index ON Photos (Style_Id);")
    
    print(t1, "Photos Table created successfully........")

    conn.commit()

    cursor.execute("DROP TABLE IF EXISTS RELATED")

    relatedsql = """CREATE TABLE RELATED(
                Related_Id SERIAL PRIMARY KEY NOT NULL,
                Current_product_id INT NOT NULL,
                Related_products_id INT NOT NULL
    )"""
    cursor.execute(relatedsql)


    with open("/home/andrewsittner/SDCCSVS/related.csv", 'r') as file:
        Related_insert_script = 'INSERT INTO RELATED (Related_Id, Current_product_id, Related_products_id) VALUES (%s, %s, %s);'
        count = 0
        values = []
        csvreader = csv.reader(file)
        for row in csvreader:
            if count > 0:
                values.append((row[0], row[1], row[2]))
            count = 1
            if len(values) == 1000:
                psycopg2.extras.execute_batch(cursor, Related_insert_script, values, page_size=1000)
                del(values)
                values = []
        if len(values) > 0:
            psycopg2.extras.execute_batch(cursor, Related_insert_script, values, page_size=1000)
            del(values)
            values = []
    t1 = datetime.datetime.now()-t0
    cursor.execute("CREATE INDEX Related_Index ON RELATED (Current_product_id);")
    print(t1, "Related Table created successfully........")
    conn.commit()
# Closing the connection
    conn.close()


except Exception as error:
    print(error)
finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()

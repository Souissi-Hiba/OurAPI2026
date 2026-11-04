import pymysql


# Keeps the database settings in one place.
def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="root123",
        database="university",
        cursorclass=pymysql.cursors.DictCursor,
    )

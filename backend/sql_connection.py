import mysql.connector
__cnx = None

# function to connect to a local server
def get_sql_connection():
    global __cnx
    if __cnx is None:
        __cnx = mysql.connector.connect(user='root', password='shailesh', host='127.0.0.1', database='grocery_store')
    return __cnx
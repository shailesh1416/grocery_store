from sql_connection import get_sql_connection


# get all uom
def get_uoms(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM uom")
    cursor.execute(query)

    response = []
    for (uom_id,uom_name) in cursor:
        response.append({
            'uom_id':uom_id,
            'uom_name':uom_name
        })
    return response

if __name__=='__main__':
    connection = get_sql_connection()
    print(get_uoms(connection))
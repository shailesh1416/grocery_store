from sql_connection import get_sql_connection


# Function to get all products
def get_all_products(connection):

    cursor = connection.cursor()
    query = "SELECT p.product_id,p.name,p.rate, u.uom_name FROM grocery_store.products as p inner join grocery_store.uom as u on p.uom_id = u.uom_id;"
    cursor.execute(query)
    response = []
    for (pid,name,rate,unit) in cursor:
        response.append(
            {
                'product_id':pid,
                'name' : name,
                'rate':rate,
                'uom_name':unit,
            }
        )
    return response

# Function to get single products
def get_product(connection,product_id):
    cursor = connection.cursor()
    query = ("SELECT product_id,name,rate FROM grocery_store.products where product_id="+str(product_id))
    cursor.execute(query)
    data = cursor.fetchone()
    response={
            'name' : data[0],
            'rate':data[1],
            'uom_name':data[2],
        }
    return response

# Function to insert a products
def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("insert into products"
             "(name,uom_id,rate)"
             "values(%s,%s,%s)")
    data = (product['name'],product['uom_id'],product['rate'])
    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid

# Delete a product

def delete_product(connection,product_id):
    cursor = connection.cursor()
    query = ("delete from products where product_id="+str(product_id))
    cursor.execute(query)
    connection.commit()
    return cursor.lastrowid


if __name__=='__main__':
    pass
    # connection = get_sql_connection()
    # print(get_all_products(connection))
    # print(insert_new_product(connection,{
    #     'uom_id':'1',
    #     'name':'cabbage',
    #     'rate':'10'
    # }))
    # print(delete_product(connection, 13))
    # print(get_product(connection, 18))


    connection.close()


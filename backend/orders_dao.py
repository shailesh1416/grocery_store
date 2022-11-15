from sql_connection import get_sql_connection
from datetime import datetime

# Function to get all products
def get_all_orders(connection):
    cursor = connection.cursor()
    query = "select * from orders order by datetime desc"
    cursor.execute(query)
    response = []
    for (order_id,customer_name,total,datetime,status) in cursor:
        response.append(
            {
                'order_id':order_id,
                'customer_name' : customer_name,
                'total':total,
                'datetime':datetime,
                'status':status
            }
        )
    return response

#get order details
def get_order_details(connection,order_id):
    cursor = connection.cursor()
    query = ("SELECT o.order_id,o.quantity,o.total_price, p.name FROM grocery_store.order_details as o inner join grocery_store.products as p on o.product_id = p.product_id where order_id="+str(order_id))
    cursor.execute(query)
    response = []
    for (order_id,quantity,total_price,product_name) in cursor:
        response.append(
            {
                'order_id':order_id,
                'product_name':product_name,
                'quantity':quantity,
                'total_price':total_price,
            }
        )
    return response

# order cancled
def cancle_order(connection,order_id):
    cursor = connection.cursor()
    query = ("update grocery_store.orders set status=2 where order_id="+str(order_id))
    cursor.execute(query)
    connection.commit()
    return cursor.lastrowid

# order completed
def order_done(connection,order_id):
    cursor = connection.cursor()
    query = ("update grocery_store.orders set status=1 where order_id="+str(order_id))
    cursor.execute(query)
    # update inventory once order is completed
    query = ("SELECT product_id,quantity FROM grocery_store.order_details where order_id="+str(order_id))
    cursor.execute(query)
    items = []
    for (product_id,quantity) in cursor:
        items.append([ product_id,quantity])

    for (product_id,quantity) in items:
        # print(1)
        # print(str(product_id),quantity)
        cursor = connection.cursor()
        sale1_query = ("select sale from grocery_store.products where product_id="+str(product_id))
        cursor.execute(sale1_query)
        # print(cursor.fetchone()[0])
        prevQuantity = cursor.fetchone()[0]
        sale2_query = ("UPDATE products SET sale = %s where product_id=%s")
        data = (str(int(quantity)+prevQuantity),str(product_id))
        cursor.execute(sale2_query,data)
    connection.commit()
    return cursor.lastrowid


# insert orders
def insert_order(connection,order):
    cursor = connection.cursor()
    order_query = ("INSERT INTO orders"
                "(customer_name,total,datetime)"
                "VALUES(%s,%s,%s)")
    order_data = (order['customer_name'],order['grand_total'],datetime.now())
    cursor.execute(order_query,order_data)
    order_id = cursor.lastrowid
    
    order_details_query = ("INSERT INTO order_details (order_id,product_id,quantity,total_price) values(%s,%s,%s,%s)")
    order_details_data = []

    for item in order['order_details']:
        order_details_data.append([
            order_id,
            int(item['product_id']),
            float(item['quantity']),
            float(item['total_price'])
        ])
        # sale1_query = ("select sale from products where product_id="+str(item['product_id']))
        # cursor.execute(sale1_query)
        # prevQuantity = cursor.fetchone()[0]
        # sale2_query = ("UPDATE products SET sale = %s where product_id=%s")
        # data = (str(int(item['quantity'])+prevQuantity),str(item['product_id']))
        # cursor.execute(sale2_query,data)
    # inserting multiple recored
    cursor.executemany(order_details_query,order_details_data)
    connection.commit()
    return order_id

if __name__=='__main__':
    pass
    # connection = get_sql_connection()
    # print(get_all_orders(connection))
    # print(insert_order(connection,{
    #     'customer_name':'Hulk',
    #     'total':'500',
    #     'datetime':datetime.now(),
    #     'order_details':[
    #         {
    #             'product_id':1,
    #             'quantity':2,
    #             'total_price':50
    #         },
    #         {
    #             'product_id':3,
    #             'quantity':1,
    #             'total_price':20
    #         }
    #     ]
    # }))
    # print(delete_product(connection, 13))


    # connection.close()

from sql_connection import get_sql_connection
from datetime import datetime

# Function to get all products
def get_all_orders(connection):
    cursor = connection.cursor()
    query = "select * from orders"
    cursor.execute(query)
    response = []
    for (order_id,customer_name,total,datetime) in cursor:
        response.append(
            {
                'order_id':order_id,
                'customer_name' : customer_name,
                'total':total,
                'datetime':datetime,
            }
        )
    return response

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


    connection.close()

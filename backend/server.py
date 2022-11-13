from flask import Flask, request, jsonify,json
from  products_dao import get_all_products,delete_product,insert_new_product,get_product,edit_product
from  orders_dao import get_all_orders,insert_order,get_order_details
from  uom_dao import get_uoms

from sql_connection import get_sql_connection
app = Flask(__name__)

# connecting to database

# route for geting all products
@app.route("/getProducts", methods=['GET'])
def getProducts():
    connection = get_sql_connection()
    products = get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin','*')
    connection.close
    return response

# route for geting all orders
@app.route("/getAllOrders", methods=['GET'])
def getOrders():
    connection  = get_sql_connection()
    orders = get_all_orders(connection)
    response = jsonify(orders)
    response.headers.add('Access-Control-Allow-Origin','*')
    connection.close()
    return response

# route for geting orders details
@app.route("/orderDetails", methods=['GET'])
def getOrderDetails():
    order_id = request.args.get("order_id")
    connection  = get_sql_connection()
    orders = get_order_details(connection,order_id)
    response = jsonify(orders)
    response.headers.add('Access-Control-Allow-Origin','*')
    connection.close()
    return response

# route to get a product
@app.route("/getProduct", methods=['GET'])
def getProduct():
    connection  = get_sql_connection()
    product_id = request.args.get("product_id")
    product = get_product(connection,product_id)
    response = jsonify({
        'data': product,
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    connection.close()
    return response

# route to delete a product
@app.route("/deleteProduct", methods=['POST'])
def deleteProduct():
    connection = get_sql_connection()
    return_id = delete_product(connection,request.form['product_id'])
    response = jsonify({
        'product_id': return_id,
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    connection.close()
    return response

# route to get all units
@app.route("/getUOM", methods=['GET'])
def getUoms():
    connection = get_sql_connection()
    uoms = get_uoms(connection)
    response = jsonify(uoms)
    response.headers.add('Access-Control-Allow-Origin','*')
    connection.close()
    return response

# route to insert a product
@app.route("/insertProduct", methods=['POST'])
def insertProduct():
    connection  = get_sql_connection()
    product_payload = json.loads(request.form['data'])
    return_id = insert_new_product(connection,product_payload)
    response = jsonify({
        'product_id': return_id,
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    connection.close()
    return response

# route to edit a product
@app.route("/editProduct", methods=['POST'])
def editProduct():
    connection  = get_sql_connection()
    product_payload = json.loads(request.form['data'])
    return_id = edit_product(connection,product_payload)
    response = jsonify({
        'product_id': return_id,
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    connection.close()
    return response


# route to insert a order
@app.route("/insertOrder", methods=['POST'])
def insertOrer():
    connection  = get_sql_connection()
    order_payload = json.loads(request.form['data'])
    order_id = insert_order(connection,order_payload)
    response = jsonify({
        'order_id': order_id,
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    connection.close()
    return response
if __name__=='__main__':
    print("Starting Python Flask server for Grocery Store management system.")
    app.run(port=5000)
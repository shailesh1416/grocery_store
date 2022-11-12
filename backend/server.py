from flask import Flask, request, jsonify,json
from  products_dao import get_all_products,delete_product,insert_new_product,get_product
from  orders_dao import get_all_orders,insert_order
from  uom_dao import get_uoms

from sql_connection import get_sql_connection
app = Flask(__name__)

# connecting to database
connection = connection = get_sql_connection()

# route for geting all products
@app.route("/getProducts", methods=['GET'])
def getProducts():
    products = get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

# route for geting all orders
@app.route("/getAllOrders", methods=['GET'])
def getOrders():
    orders = get_all_orders(connection)
    response = jsonify(orders)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

# route to get a product
@app.route("/getProduct", methods=['POST'])
def getProduct():
    product = get_product(connection,request.form['product_id'])
    response = jsonify({
        'data': product,
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

# route to delete a product
@app.route("/deleteProduct", methods=['POST'])
def deleteProduct():
    return_id = delete_product(connection,request.form['product_id'])
    response = jsonify({
        'product_id': return_id,
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

# route to get all units
@app.route("/getUOM", methods=['GET'])
def getUoms():
    uoms = get_uoms(connection)
    response = jsonify(uoms)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

# route to insert a product
@app.route("/insertProduct", methods=['POST'])
def insertProduct():
    product_payload = json.loads(request.form['data'])
    return_id = insert_new_product(connection,product_payload)
    response = jsonify({
        'product_id': return_id,
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

# route to insert a order
@app.route("/insertOrder", methods=['POST'])
def insertOrer():
    order_payload = json.loads(request.form['data'])
    order_id = insert_order(connection,order_payload)
    response = jsonify({
        'order_id': order_id,
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response
if __name__=='__main__':
    print("Starting Python Flask server for Grocery Store management system.")
    app.run(port=5000)
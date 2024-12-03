from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_connection import get_sql_connection
import json
import os

import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)
CORS(app)

def get_db():
    return get_sql_connection()

@app.route('/getUOM', methods=['GET'])
def get_uom():
    connection = get_db()
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    return response

@app.route('/getProducts', methods=['GET'])
def get_products():
    connection = get_db()
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    connection = get_db()
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    connection = get_db()
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    connection = get_db()
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    connection = get_db()
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(host='0.0.0.0', port=5000)
else:
    # For gunicorn
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

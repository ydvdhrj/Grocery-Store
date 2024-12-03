from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.sql_connection import get_sql_connection
import json
import os
import logging

import backend.products_dao as products_dao
import backend.orders_dao as orders_dao
import backend.uom_dao as uom_dao

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def get_db():
    try:
        return get_sql_connection()
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

@app.route('/getUOM', methods=['GET'])
def get_uom():
    try:
        connection = get_db()
        response = uom_dao.get_uoms(connection)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in get_uom: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/getProducts', methods=['GET'])
def get_products():
    try:
        connection = get_db()
        response = products_dao.get_all_products(connection)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in get_products: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    try:
        connection = get_db()
        request_payload = json.loads(request.form['data'])
        product_id = products_dao.insert_new_product(connection, request_payload)
        return jsonify({'product_id': product_id})
    except Exception as e:
        logger.error(f"Error in insert_product: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    try:
        connection = get_db()
        response = orders_dao.get_all_orders(connection)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in get_all_orders: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    try:
        connection = get_db()
        request_payload = json.loads(request.form['data'])
        order_id = orders_dao.insert_order(connection, request_payload)
        return jsonify({'order_id': order_id})
    except Exception as e:
        logger.error(f"Error in insert_order: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    try:
        connection = get_db()
        return_id = products_dao.delete_product(connection, request.form['product_id'])
        return jsonify({'product_id': return_id})
    except Exception as e:
        logger.error(f"Error in delete_product: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

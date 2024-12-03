from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from backend import sql_connection
from backend import products_dao
from backend import orders_dao
from backend import uom_dao
from backend import users_dao
import json
import os
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../ui')
CORS(app)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.name = user_data['name']
        self.email = user_data['email']

@login_manager.user_loader
def load_user(user_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        return User({'id': user_data[0], 'name': user_data[1], 'email': user_data[2]})
    return None

def get_db():
    try:
        return sql_connection.get_sql_connection()
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

@app.route('/')
def serve_ui():
    return send_from_directory('../ui', 'login.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../ui', path)

@app.route('/api/check-auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'name': current_user.name,
                'email': current_user.email
            }
        })
    return jsonify({'authenticated': False}), 401

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400
        
        connection = get_db()
        user_data, error = users_dao.verify_user(connection, email, password)
        
        if error:
            logger.error(f"Login error: {error}")
            return jsonify({'message': error}), 401
        
        user = User(user_data)
        login_user(user)
        return jsonify({
            'message': 'Login successful',
            'user': {
                'name': user.name,
                'email': user.email
            }
        }), 200
    except Exception as e:
        logger.error(f"Unexpected login error: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not name or not email or not password:
            return jsonify({'message': 'All fields are required'}), 400
        
        connection = get_db()
        success, message = users_dao.create_user(connection, name, email, password)
        
        if success:
            return jsonify({'message': message}), 200
        
        logger.error(f"Registration error: {message}")
        return jsonify({'message': message}), 400
    except Exception as e:
        logger.error(f"Unexpected registration error: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/getProducts', methods=['GET'])
@login_required
def get_products():
    try:
        connection = get_db()
        products = products_dao.get_all_products(connection)
        return jsonify(products), 200
    except Exception as e:
        logger.error(f"Error in get_products: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/insertProduct', methods=['POST'])
@login_required
def insert_product():
    try:
        connection = get_db()
        product_details = request.json
        product_id = products_dao.insert_new_product(connection, product_details)
        return jsonify({"product_id": product_id}), 200
    except Exception as e:
        logger.error(f"Error in insert_product: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/deleteProduct', methods=['POST'])
@login_required
def delete_product():
    try:
        connection = get_db()
        product_id = request.json['product_id']
        products_dao.delete_product(connection, product_id)
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error in delete_product: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/getAllOrders', methods=['GET'])
@login_required
def get_all_orders():
    try:
        connection = get_db()
        orders = orders_dao.get_all_orders(connection)
        return jsonify(orders), 200
    except Exception as e:
        logger.error(f"Error in get_all_orders: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/insertOrder', methods=['POST'])
@login_required
def insert_order():
    try:
        connection = get_db()
        order_details = request.json
        order_id = orders_dao.insert_order(connection, order_details)
        return jsonify({"order_id": order_id}), 200
    except Exception as e:
        logger.error(f"Error in insert_order: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/getUOM', methods=['GET'])
@login_required
def get_uom():
    try:
        connection = get_db()
        uom_list = uom_dao.get_uoms(connection)
        return jsonify(uom_list), 200
    except Exception as e:
        logger.error(f"Error in get_uom: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    print(f"Static folder: {app.static_folder}")
    print(f"Current working directory: {os.getcwd()}")
    app.run(host='0.0.0.0', port=port, debug=True)

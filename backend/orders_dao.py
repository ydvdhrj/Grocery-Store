from datetime import datetime
from sql_connection import get_sql_connection
import psycopg2

def get_all_orders(connection):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT o.order_id, o.customer_name, o.total, o.datetime,
            od.product_id, od.quantity, od.total_price,
            p.name, p.price_per_unit
        FROM orders o
        INNER JOIN order_details od ON o.order_id = od.order_id
        INNER JOIN products p ON od.product_id = p.product_id
    """
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    
    response = {}
    for record in records:
        order_id = record['order_id']
        if order_id not in response:
            response[order_id] = {
                'order_id': record['order_id'],
                'customer_name': record['customer_name'],
                'order_date': record['datetime'],
                'total': float(record['total']),
                'order_details': []
            }
        
        response[order_id]['order_details'].append({
            'product_id': record['product_id'],
            'quantity': float(record['quantity']),
            'total_price': float(record['total_price']),
            'product_name': record['name'],
            'price_per_unit': float(record['price_per_unit'])
        })
    
    return list(response.values())

def insert_order(connection, order):
    cursor = connection.cursor()
    
    # Insert into orders table
    order_query = """
        INSERT INTO orders (customer_name, total)
        VALUES (%s, %s)
        RETURNING order_id
    """
    order_data = (order['customer_name'], order['grand_total'])
    
    cursor.execute(order_query, order_data)
    order_id = cursor.fetchone()[0]
    
    # Insert order details
    order_details_query = """
        INSERT INTO order_details (order_id, product_id, quantity, total_price)
        VALUES (%s, %s, %s, %s)
    """
    
    order_details_data = []
    for order_detail in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail['product_id']),
            float(order_detail['quantity']),
            float(order_detail['total_price'])
        ])
    
    cursor.executemany(order_details_query, order_details_data)
    
    connection.commit()
    cursor.close()
    
    return order_id

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
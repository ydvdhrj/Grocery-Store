from backend.sql_connection import get_sql_connection
import psycopg2

def get_uoms(connection):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "SELECT * FROM uom"
    cursor.execute(query)
    response = cursor.fetchall()
    cursor.close()
    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_uoms(connection))
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection configuration
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'bartar20@CS',
    'host': '10.10.248.114',
    'port': '5432'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**db_config)
        print("Database connection successful")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/get_info/<int:user_id>', methods=['GET'])
def get_info(user_id):
    print(f"User {user_id} sent request.")
    return jsonify({'info': 'Hello from server!'})

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    print("Received a request!")
    try:
        conn = get_db_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return jsonify({'error': 'Failed to connect to the database'}), 500

        cursor = conn.cursor()

        if request.method == 'GET':
            # Fetch data from the database
            cursor.execute("SELECT * FROM users;")
            rows = cursor.fetchall()
            print(f"Fetched rows: {rows}")
            return jsonify(rows)
        elif request.method == 'POST':
            # Insert data into the database
            data = request.json
            print(f"Data received: {data}")

            if not all(key in data for key in ('username', 'password')):
                print("Missing required fields in the data.")
                return jsonify({'error': 'Missing required fields'}), 400

            # Check if the username already exists
            cursor.execute("SELECT id FROM users WHERE username = %s;", (data['username'],))
            if cursor.fetchone() is not None:
                print("Username already exists.")
                return jsonify({'error': 'Username already exists'}), 409

            try:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;",
                    (data['username'], data['password'])
                )
                new_id = cursor.fetchone()[0]
                conn.commit()
                print('Data inserted successfully')
                return jsonify({'status': 'Data inserted successfully', 'id': new_id})
            except Exception as e:
                print(f"Error during data insertion: {e}")
                return jsonify({'error': f'Failed to insert data: {e}'}), 500
    except Exception as e:
        print(f"Database operation failed: {e}")
        return jsonify({'error': f'Failed to communicate with the database: {e}'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(f"Login data received: {data}")

    if not all(key in data for key in ('username', 'password')):
        print("Missing required fields in the data.")
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return jsonify({'error': 'Failed to connect to the database'}), 500

        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username = %s AND password = %s;",
            (data['username'], data['password'])
        )
        user = cursor.fetchone()

        if user:
            print(f"User {data['username']} logged in successfully")
            return jsonify({'status': 'Login successful', 'id': user[0]})
        else:
            print(f"Invalid login for user {data['username']}")
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'error': f'Failed to login: {e}'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    print('app runs on port 80...')

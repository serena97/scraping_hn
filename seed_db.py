import psycopg2

# Database connection parameters
dbname = "my_database"
user = "user"
password = "password"
host = "localhost"
port = "5433"  # Make sure this matches the port you've exposed in Docker

# SQL query to create a table
create_table_query = '''
CREATE TABLE IF NOT EXISTS web_data (
    url VARCHAR(255),
    title TEXT,
    body TEXT,
    comments TEXT
)
'''

# Connect to PostgreSQL and create the table
try:
    # Connect to the database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Create the table
    cur.execute(create_table_query)
    print("Table created successfully")

    # Close the cursor and connection
    conn.commit()
    
    cur.execute("SELECT * FROM web_data;")
    print("Table exists and can be queried.")
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")

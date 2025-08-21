import psycopg2
class Db:
    db_name: str
    db_password: str
    db_user: str
    db_host: str
    db_port: str
    conn: any
    def __init__(self, db_name, db_user, db_password, db_host='localhost', db_port='5432'):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.conn = None
        self.connect()
    
    def connect(self):
        """Connect to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            print("Database connection established.")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            self.conn = None
        
    def insert_user(self, username, balance):
        """Insert a new user into the database."""
        if self.conn is None:
            print("No database connection.")
            return
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO user_balances (username, balance) VALUES (%s, %s)", (username, balance))
            self.conn.commit()
            cur.close()
            print(f"User {username} inserted successfully.")
        except psycopg2.Error as e:
            print(f"Error inserting user: {e}")
    
    def get_user(self, username):
        """Retrieve a user from the database by username."""
        if self.conn is None:
            print("No database connection.")
            return None
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT username, balance FROM user_balances WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            if user:
                return {"username": user[0], "balance": user[1]}
            else:
                print(f"User {username} not found.")
                return None
        except psycopg2.Error as e:
            print(f"Error retrieving user: {e}")
            return None
    
    def delete_user(self, username):
        """Delete a user from the database by username."""
        if self.conn is None:
            print("No database connection.")
            return
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM user_balances WHERE username = %s", (username,))
            self.conn.commit()
            cur.close()
            print(f"User {username} deleted successfully.")
        except psycopg2.Error as e:
            print(f"Error deleting user: {e}")
        
    def add_product_at_list(self, product_name, price, username):
        """Add a product to the username's products list in the database."""
        if self.conn is None:
            print("No database connection.")
            return
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO products (product_name, price, username) VALUES (%s, %s, %s)", (product_name, price, username))
            self.conn.commit()
            cur.close()
            print(f"Product {product_name} added successfully for user {username}.")
        except psycopg2.Error as e:
            print(f"Error adding product: {e}")


    def buy_product(self, username, product_id, product_list):
        """Process a purchase of a product by a user from product list."""
        if self.conn is None:
            print("No database connection.")
            return
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT price FROM products WHERE id = %s AND username = %s", (product_id, username))
            product = cur.fetchone()
            if product:
                price = product[0]
                cur.execute("UPDATE user_balances SET balance = balance - %s WHERE username = %s", (price, username))
                self.conn.commit()
                print(f"Product {product_id} purchased successfully by {username}.")
            else:
                print(f"Product {product_id} not found for user {username}.")
            cur.close()
        except psycopg2.Error as e:
            print(f"Error processing purchase: {e}")


            
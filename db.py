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
        
    def add_product_at_list(self, product_name, price):
        """Add a product to list in the database."""
        if self.conn is None:
            print("No database connection.")
            return
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO products (product_name, price) VALUES (%s, %s)", (product_name, price))
            self.conn.commit()
            cur.close()
            print(f"Product {product_name} added successfully.")
        except psycopg2.Error as e:
            print(f"Error adding product: {e}")


    def buy_product(self, user_balances_id:int, product_id:int):
        """Buy a product from list in the database."""
        if self.conn is None:
            print("No database connection.")
            return
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO shoppings (user_balances_id, product_id) VALUES (%s, %s)", (user_balances_id, product_id))
            self.conn.commit()
            cur.close()
            print(f"Product with id {product_id} bought successfully by user with id {user_balances_id}.")
        except psycopg2.Error as e:
            print(f"Error buying product: {e}")
     


            
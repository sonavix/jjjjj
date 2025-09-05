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
        
    def add_product(self, product_name, price):
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

    def get_product(self, product_name):
        """Retrieve a product from the database by product_name."""
        if self.conn is None:
            print("No database connection.")
            return None
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT product_name, price FROM products WHERE product_name = %s", (product_name,))
            product = cur.fetchone()
            cur.close()
            if product:
                return {"product_name": product[0], "price": product[1]}
            else:
                print(f"Product {product_name} not found.")
                return None
        except psycopg2.Error as e:
            print(f"Error retrieving product: {e}")
            return None
    def add_product_to_shopping(self, username, product):
        """Add a product to shopping list in the database."""
        if self.conn is None:
            print("No database connection.")
            return
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id FROM user_balances WHERE username = %s", (username,))
            user = cur.fetchone()
            if not user:
                print(f"User {username} not found.")
                cur.close()
                return
            user_id = user[0]
            cur.execute("SELECT id FROM products WHERE product_name = %s", (product,))
            prod = cur.fetchone()
            if not prod:
                print(f"Product {product} not found.")
                cur.close()
                return
            product_id = prod[0]
            cur.execute("INSERT INTO shoppings (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
            self.conn.commit()
            cur.close()
            print(f"Product {product} added to shopping list for user {username}.")
        except psycopg2.Error as e:
            print(f"Error adding product to shopping list: {e}")
 
    def buy_product(self, user_id, product_id):
        """Buy a product for a user, deducting the price from their balance."""
        if self.conn is None:
            print("No database connection.")
            return
        try:
            cur = self.conn.cursor()
            # Get user balance
            cur.execute("SELECT balance FROM user_balances WHERE id = %s", (user_id,))
            user = cur.fetchone()
            if not user:
                print(f"User with ID {user_id} not found.")
                cur.close()
                return
            balance = user[0]
            # Get product price
            cur.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            product = cur.fetchone()
            if not product:
                print(f"Product with ID {product_id} not found.")
                cur.close()
                return
            price = product[0]
            # Check if user has enough balance
            if balance < price:
                print(f"User with ID {user_id} has insufficient balance.")
                cur.close()
                return
            # Deduct price from user balance
            new_balance = balance - price
            cur.execute("UPDATE user_balances SET balance = %s WHERE id = %s", (new_balance, user_id))
            # Remove product from shopping list
            cur.execute("DELETE FROM shoppings WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            self.conn.commit()
            cur.close()
            print(f"User with ID {user_id} bought product with ID {product_id}. New balance: {new_balance}.")
        except psycopg2.Error as e:
            print(f"Error processing purchase: {e}")

        

     
    def delete_product(self, product_name):
        """Delete a product from the database by product_name."""
        if self.conn is None:
            print("No database connection.")
            return 
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM products WHERE product_name = %s", (product_name,))
            self.conn.commit()
            cur.close()
            print(f"Product {product_name} deleted successfully.")
        except psycopg2.Error as e:
            print(f"Error deleting product: {e}")

            
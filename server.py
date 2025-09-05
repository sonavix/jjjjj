from db import Db
from typing import List
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

# Класс пользователя
class User:
    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance

db: Db = Db(db_name="users", db_user="sofia", db_password="nigga")

class SimpleHandler(BaseHTTPRequestHandler):

    # Метод POST — добавление нового пользователя
    def do_POST(self):
        parsed_url = urlparse(self.path)
        path_parts = parsed_url.path.strip("/").split("/")


        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length)

        try:
            data = json.loads(post_body.decode())
            response = {}
            match path_parts[0]:
                case "user":
                    name = data.get("name")
                    balance = data.get("balance", 0)
                    if not name or balance < 0:
                        raise ValueError("wrong user data")
                    db.insert_user(name, balance) 
                    response = {
                        "message": "User created successfully",
                        "user": {
                            "name": name,
                            "balance": balance
                        }
                    }
                
                case "product":
                    product_name = data.get("product_name")
                    price = data.get("price", 0)
                    if not product_name or price < 0:
                        raise ValueError("wrong product data")
                    db.add_product(product_name, price)
                    return
                case "buy":
                    user_id = data.get("username")
                    product_id = data.get("product")
                    if not user_id or not product_id:
                        raise ValueError("wrong buy data")
                    db.buy_product(user_id, product_id)
                    response = {
                        "message": f"User {user_id} bought product {product_id}"
                    }
                    
                    
                case 'cart':
                    user_id = data.get("username")
                    product_id = data.get("product")
                    if not user_id or not product_id:
                        raise ValueError("wrong cart data")
                    db.add_product_to_shopping(user_id, product_id)
                    response = {
                        "message": f"Products {product_id} added to shopping list for user {user_id}"
                    }

                case _: # The wildcard or default case
                    raise ValueError("Неправильный путь. Используйте /user, /product или /buy")
                


            

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    # Метод GET — получить пользователя по имени и балансу
    def do_GET(self):

        parsed_url = urlparse(self.path)
        path_parts = parsed_url.path.strip("/").split("/")
        path1 = path_parts[0] if len(path_parts) > 0 else None
        path2 = path_parts[1] if len(path_parts) > 1 else None
    

        if not path1:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Username is missing"}).encode())
            return

        
        if path1 == "user":
            user = db.get_user(path2)
            if path2 == user:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(user).encode())
        

        if path1 == "product":
            product = db.get_product(path2)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(product).encode())


            

 
        
        else:

            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Пользователь не найден"}).encode())

    # 🔥 Метод DELETE — удалить пользователя по имени
    def do_DELETE(self):
        parsed_url = urlparse(self.path)
        path_parts = parsed_url.path.strip("/").split("/")

        if len(path_parts) != 2:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Неправильный путь. Используйте /username"}).encode())
            return

        command = path_parts[0]
        stuff = path_parts[1]
        global db

        if command == "user":
            user = db.delete_user(stuff)
            if user:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": f"Пользователь {stuff} удален"}).encode())
            else:

                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Пользователь не найден"}).encode())
        if command == "product":
            db.delete_product(stuff)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"Продукт {stuff} удален"}).encode())
    
        else:

            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Неправильный путь. Используйте /user/username или /product/productname"}).encode())



"""
    def add_product(self, product_name, price):
       
        if not product_name or price < 0:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Неверные данные продукта"}).encode())
            return

        db.add_product(product_name, price)
        self.send_response(202)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": f"Продукт {product_name} добавлен"}).encode())

    def buy_product(self, username, product_name):

        if not username or not product_name:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Неверные данные пользователя или продукта"}).encode())
            return

        user = db.get_user(username)
        if not user:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Пользователь не найден"}).encode())
            return

        # Логика покупки продукта
        # ...

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": f"Пользователь {username} купил продукт {product_name}"}).encode())
"""
# Запуск сервера
server = HTTPServer(("localhost", 8000), SimpleHandler)
print("Сервер запущен: http://localhost:8000/")
server.serve_forever()
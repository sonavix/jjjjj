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
                    self.add_product(product_name, price)
                    return
                case "buy":
                    username = data.get("username")
                    product_name = data.get("product_name")
                    if not username or not product_name:
                        raise ValueError("wrong buy data")
                    self.buy_product(username, product_name)
                    return
                
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

        username = path_parts[0] if len(path_parts) > 0 else None
        stuff = path_parts[1] if len(path_parts) > 1 else None


        if not username:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Username is missing"}).encode())
            return

        user = db.get_user(username)
        if username == "user":
            if stuff == user:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(user).encode())
        
        if username == "buy":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(user).encode())

        if username == "product":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(user).encode())

        
        
        else:

            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Пользователь не найден"}).encode())

    # 🔥 Метод DELETE — удалить пользователя по имени
    def do_DELETE(self):
        parsed_url = urlparse(self.path)
        path_parts = parsed_url.path.strip("/").split("/")

        if len(path_parts) != 1:
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
            product = db.delete_product(stuff)
            if product:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": f"Продукт {stuff} удален"}).encode())
            else:

                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Продукт не найден"}).encode())
        else:

            self.send_response(400)
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
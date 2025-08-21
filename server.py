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

users: Db = Db(db_name="users", db_user="sofia", db_password="nigga")

class SimpleHandler(BaseHTTPRequestHandler):

    # Метод POST — добавление нового пользователя
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length)

        try:
            data = json.loads(post_body.decode())  # Читаем JSON из запроса
            name = data.get("name")
            balance = data.get("balance", 0)

            if not name:
                raise ValueError("Поле 'name' обязательно")

            users.insert_user(name, balance)  # Добавляем пользователя в базу данных
                                 # Добавляем пользователя в список

            response = {
                "message": "Пользователь создан",
                "user": {
                    "name": name,
                    "balance": balance
                }
            }

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


        if not username:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Username is missing"}).encode())
            return

        user = users.get_user(username)
        if user:
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

        username = path_parts[0]
        global users

        # Проверка: существует ли пользователь
        user = users.delete_user(username)
        if user:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"Пользователь {username} удален"}).encode())
        else:

            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Пользователь не найден"}).encode())

    def add_product(self, product_name, price):
        """Добавление нового продукта в базу данных."""
        if not product_name or price < 0:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Неверные данные продукта"}).encode())
            return

        users.add_product(product_name, price)
        self.send_response(202)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": f"Продукт {product_name} добавлен"}).encode())

    def buy_product(self, username, product_name):
        """Покупка продукта пользователем."""
        if not username or not product_name:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Неверные данные пользователя или продукта"}).encode())
            return

        user = users.get_user(username)
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

# Запуск сервера
server = HTTPServer(("localhost", 8000), SimpleHandler)
print("Сервер запущен: http://localhost:8000/")
server.serve_forever()
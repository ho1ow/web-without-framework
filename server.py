import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib
from db.database import *
from util.jwt import *
import logging

logging.basicConfig(level=logging.INFO)


class Server(SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        try:
            if self.path == '/':
                self.path = '/static/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            elif self.path == '/register':
                self.path = '/static/register.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            elif self.path == '/login':
                self.path = '/static/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            elif self.path == '/get_tasks':
                username = verify_user(self)
                if not username:
                    self.send_json({"error": "Unauthorized"}, 401)
                    return
                tasks = get_tasks(username)
                self.send_json([{'id': task[0], 'description': task[1]}
                               for task in tasks])
            elif self.path == '/tasks':
                self.path = '/static/task.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                SimpleHTTPRequestHandler.do_GET(self)
        except Exception as e:
            logging.error(f"Error during GET request: {str(e)}")
            self.send_json({"error": "Server error"}, 500)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data_dict = urllib.parse.parse_qs(post_data)

        try:
            if self.path == '/login' or self.path == '/register':
                self.handle_auth(data_dict, self.path)
            elif self.path == '/add':
                self.handle_add_task(data_dict)
        except Exception as e:
            logging.error(f"Error during POST request: {str(e)}")
            self.send_json({"error": "Server error"}, 500)

    def handle_auth(self, data, path):
        if 'username' in data and 'password' in data:
            username, password = data['username'][0], data['password'][0]
            if path == '/login':
                success, token = login(username, password)
                if success:
                    token = generate_token(
                        {'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=100000)})
                    self.send_response(302)
                    self.send_header(
                        'Set-Cookie', f'token={token}; HttpOnly; SameSite=Lax')
                    self.send_header('Content-type', 'application/json')

                    self.end_headers()
                    self.wfile.write(json.dumps(
                        {"message": "Login successful"}).encode('utf-8'))

                else:
                    self.send_json({"error": "Login failed"}, 401)

            elif path == '/register':
                success, message = register(username, password)
                self.send_json({"message": message}, 201 if success else 400)
        else:
            self.send_json({"error": "Missing username or password"}, 400)

    def handle_add_task(self, data):
        username = verify_user(self)
        if not username:
            self.send_json({"error": "Forbidden"}, 403)
            return
        description = data.get('description', [None])[0]
        if not description:
            self.send_json({"error": "Description is required"}, 400)
            return
        add_task(username, description)
        self.send_json({"message": "Task added successfully"}, 201)

    def do_DELETE(self):
        if self.path.startswith('/delete/'):
            username = verify_user(self)
            if not username:
                self.send_json({"error": "Unauthorized"}, 401)
                return

            try:
                task_id = self.path.split('/')[-1]
                if not task_id.isdigit():
                    raise ValueError("Task ID must be a digit")

                success, msg = delete_task(username, task_id)
                if success:
                    self.send_json({"message": msg}, 200)
                else:
                    self.send_json({"error": msg}, 404)

            except ValueError as ve:
                logging.error(f"Validation error: {ve}")
                self.send_json({"error": str(ve)}, 400)
            except Exception as e:
                logging.error(f"Error in deleting task: {e}")
                self.send_json({"error": "Server error"}, 500)

        else:
            logging.info("Attempt to delete from a non-existent resource.")
            self.send_json({"error": "Resource not found"}, 404)


def run(server_class=HTTPServer, handler_class=Server):
    server_address = ('', 9999)
    httpd = server_class(server_address, handler_class)
    print("run")
    httpd.serve_forever()


if __name__ == '__main__':
    create_db()
    run()

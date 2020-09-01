import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler
from uuid import uuid4

import model.items
import model.users

tokens = {'matias': 'test'}


class ServerHTTPRequestHandler(BaseHTTPRequestHandler):

    # TODO: Implement better exception cases

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello word!')

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        body_json = json.loads(body)

        if self.path == 'register':
            username = body_json['user']
            pasw = body_json['pasw']
            salt = os.urandom(64)
            final_hash = hashlib.pbkdf2_hmac('sha512', str.encode(pasw), salt, 100000)

            try:
                model.users.insert_user(username, salt, final_hash)

                self.wfile.write(b'OK')

            except Exception as e:
                print(e)
                self.wfile.write(b'Error')
                raise e

        elif self.path == 'login':
            username = body_json['user']
            pasw = body_json['pasw']

            try:
                salt, user_hash = model.users.get_salt_hash_by_username(username)

                final_hash = hashlib.pbkdf2_hmac('sha512', str.encode(pasw), salt, 100000)

                if final_hash == user_hash:
                    token = str(uuid4())

                    tokens[username] = token
                    print(token)
                    self.wfile.write(str.encode(token))

                else:
                    self.wfile.write(b'Wrong login')

            except Exception as e:
                print(e)
                self.wfile.write(b'Error')
                raise e

        elif self.path == 'get_items':
            username = body_json['user']
            token = body_json['token']

            if username not in tokens or tokens[username] != token:
                self.wfile.write(b'login')

                return

            else:
                path = body_json['path']

                items = model.items.get_items(username, path)

                item_list = [item['name'] for item in items]

                data = json.dumps({'items': item_list})

                self.wfile.write(data.encode('utf-8'))

        elif self.path == 'insert_items':
            username = body_json['user']
            token = body_json['token']

            if username not in tokens or tokens[username] != token:
                self.wfile.write(b'login')

                return

            else:
                path = body_json['path']
                items = body_json['items']

                model.items.insert_items(username, path, items)

import http.client
import json


connection = http.client.HTTPConnection('localhost', 443, 5)

data = json.dumps({'user': 'matias', 'token': 'test', 'path': '1'})

connection.request('POST', 'get_items', data)

response = connection.getresponse()

print(response.read().decode())

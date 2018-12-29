from http.server import HTTPServer
# import ssl

from controller.ServerHTTPRequestHandler import ServerHTTPRequestHandler


def main():
    httpd = HTTPServer(('localhost', 443), ServerHTTPRequestHandler)
    # httpd.socket = ssl.wrap_socket(httpd.socket, certfile='', server_side=True)
    httpd.serve_forever()


if __name__ == '__main__':
    main()

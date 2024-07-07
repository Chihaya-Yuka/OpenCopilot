import os
import zlib
import socket
import threading
import mimetypes

class HTTPRequestHandler:
    def __init__(self, client_socket, document_root):
        self.client_socket = client_socket
        self.document_root = document_root

    def handle_request(self):
        try:
            request = self.client_socket.recv(1024).decode('utf-8')
            if not request:
                return

            request_line = request.splitlines()[0]
            method, path, _ = request_line.split()

            if method != 'GET':
                self.send_response('405 Method Not Allowed', b'Method Not Allowed')
                return

            if path == '/':
                path = '/index.html'

            file_path = os.path.join(self.document_root, path.lstrip('/'))
            if not os.path.isfile(file_path):
                self.send_response('404 Not Found', b'File Not Found')
                return

            with open(file_path, 'rb') as file:
                content = file.read()

            content_type, _ = mimetypes.guess_type(file_path)
            self.send_response('200 OK', content, content_type or 'application/octet-stream', compress=True)
        except Exception as e:
            print(f'Error handling request: {e}')
        finally:
            self.client_socket.close()

    def send_response(self, status_code, content, content_type='text/html', compress=False):
        response_line = f'HTTP/1.1 {status_code}\r\n'
        headers = f'Content-Type: {content_type}\r\n'
        headers += 'Connection: close\r\n'
        if compress:
            headers += 'Content-Encoding: deflate\r\n'
            content = zlib.compress(content)
        headers += f'Content-Length: {len(content)}\r\n'
        headers += '\r\n'
        response = response_line.encode() + headers.encode() + content
        self.client_socket.sendall(response)

class HTTPServer:
    def __init__(self, host, port, document_root):
        self.host = host
        self.port = port
        self.document_root = document_root
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f'Serving HTTP on {self.host} port {self.port} (http://{self.host}:{self.port}/) ...')

            while True:
                client_socket, client_address = self.server_socket.accept()
                handler = HTTPRequestHandler(client_socket, self.document_root)
                threading.Thread(target=handler.handle_request).start()
        except Exception as e:
            print(f'Error starting server: {e}')
        finally:
            self.server_socket.close()

if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8080
    DOCUMENT_ROOT = './public'

    server = HTTPServer(HOST, PORT, DOCUMENT_ROOT)
    server.start()

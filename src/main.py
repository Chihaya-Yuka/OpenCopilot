import os
import zlib
import socket
import threading
import mimetypes

# Server configuration
HOST = '0.0.0.0'
PORT = 8080
DOCUMENT_ROOT = os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/public'

# Helper function to send HTTP response
def send_response(client_socket, status_code, content, content_type='text/html', compress=False):
    response_line = f'HTTP/1.1 {status_code}\r\n'
    headers = f'Content-Type: {content_type}\r\n'
    headers += 'Connection: close\r\n'
    if compress:
        headers += 'Content-Encoding: deflate\r\n'
        content = zlib.compress(content)
    headers += f'Content-Length: {len(content)}\r\n'
    headers += '\r\n'
    response = response_line.encode() + headers.encode() + content
    client_socket.sendall(response)

# Function to handle client requests
def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            return

        request_line = request.splitlines()[0]
        method, path, _ = request_line.split()

        if method != 'GET':
            send_response(client_socket, '405 Method Not Allowed', b'Method Not Allowed')
            return

        if path == '/':
            path = '/index.html'

        file_path = os.path.join(DOCUMENT_ROOT, path.lstrip('/'))
        if not os.path.isfile(file_path):
            send_response(client_socket, '404 Not Found', b'File Not Found')
            return

        with open(file_path, 'rb') as file:
            content = file.read()

        content_type, _ = mimetypes.guess_type(file_path)
        send_response(client_socket, '200 OK', content, content_type or 'application/octet-stream', compress=True)
    except Exception as e:
        print(f'Error handling request: {e}')
    finally:
        client_socket.close()

# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f'Serving HTTP on {HOST} port {PORT} (http://{HOST}:{PORT}/) ...')

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    start_server()

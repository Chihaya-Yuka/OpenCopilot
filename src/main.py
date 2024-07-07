import socket

class HTTPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))

    def start(self):
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            self.handle_request(client_socket)

    def handle_request(self, client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Request: {request}")
        
        if request.startswith('GET'):
            self.handle_get(client_socket)
        else:
            self.handle_not_supported(client_socket)
        
        client_socket.close()

    def handle_get(self, client_socket):
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<html><body><h1>Hello, World!</h1></body></html>"
        )
        client_socket.sendall(response.encode('utf-8'))

    def handle_not_supported(self, client_socket):
        response = (
            "HTTP/1.1 405 Method Not Allowed\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<html><body><h1>Method Not Allowed</h1></body></html>"
        )
        client_socket.sendall(response.encode('utf-8'))

    def shutdown(self):
        self.server_socket.close()

if __name__ == "__main__":
    server = HTTPServer(host='0.0.0.0', port=8080)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Shutting down server.")
        server.shutdown()

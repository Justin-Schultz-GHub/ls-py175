import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen()

print("Server is running on 0.0.0.0:8080")

while True:
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr}')

    request = client_socket.recv(1024).decode()
    if not request or 'favicon.ico' in request:
        client_socket.close()
        continue

    request_line = request.splitlines()[0]

    response = ('HTTP/1.1 200 OK\r\n'
                'Content-Type: text/plain\r\n'
                f'Content-Length: {len(request_line)}\r\n'
                '\r\n'
                f'{request_line}')

    client_socket.sendall(response.encode())
    client_socket.close()
import socket
import random

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

    http_method = request_line.split()[0]

    path = request_line.split()[1].split('?')[0]

    parameters = {}
    queries = request_line.split()[1][2:].split('&')
    for query in queries:
        key, value = query.split('=')
        parameters[key] = value

    # print(queries)
    # print(f'Request Line: {request_line}')
    # print(f'HTTP Method: {http_method}')
    # print(f'Path: {path}')
    # print(f'Parameters: {parameters}')

    response_body = (f'Request Line: {request_line}\n'
                    f'HTTP Method: {http_method}\n'
                    f'Path: {path}\n'
                    f'Parameterss: {parameters}\n'
                    )

    for i in range(int(parameters['rolls'])):
        roll = random.randint(1, int(parameters['sides']))
        response_body += f'Roll: {roll}\n'

    response = ('HTTP/1.1 200 OK\r\n'
                'Content-Type: text/plain\r\n'
                f'Content-Length: {len(response_body)}\r\n'
                '\r\n'
                f'{response_body}\n')

    client_socket.sendall(response.encode())
    client_socket.close()
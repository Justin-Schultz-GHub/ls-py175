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

    parameters = {}

    path = request_line.split()[1].split('?')[0]

    if "?" in request_line.split()[1]:
        queries = request_line.split()[1].split('?')[1].split('&')

        for query in queries:
            key, value = query.split('=')
            parameters[key] = value
    else:
        parameters['number'] = '0'

    number = int(parameters.get('number', 0))

    response_body = ("<html><head><title>Counter</title><head><body>"
                    f'<h1>HTTP Request Information</h1>'
                    f'<p><strong>Request Line: {request_line}\n</strong></p>'
                    f'<p><strong>HTTP Method: {http_method}\n</strong></p>'
                    f'<p><strong>Path: {path}\n</strong></p>'
                    f'<p><strong>Parameters: {parameters}\n</strong></p>'
                    "<h2>Counter</h2>"
                    f'<p style="color: red;">The current number is: {number}</p>'
                    f'<a href="?number={number + 1}">Add One</a>'
                    "&nbsp;&nbsp;"
                    f'<a href="?number={number - 1}">Subtract One</a>'
                    "</body></html>"
                    )

    response = ('HTTP/1.1 200 OK\r\n'
                'Content-Type: text/html\r\n'
                f'Content-Length: {len(response_body)}\r\n'
                '\r\n'
                f'{response_body}\n')

    client_socket.sendall(response.encode())
    client_socket.close()
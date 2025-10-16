import socket
import sys
import os

def main():
    if len(sys.argv) != 5:
        print("Usage: python client.py server_host server_port url_path directory")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    url_path = sys.argv[3]
    directory = sys.argv[4]
    save_directory = directory

    # ensure save_directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # create tcp socket and connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    # send get request
    request = f'GET {url_path} HTTP/1.1\r\nHost: {server_host}\r\nConnection: close\r\n\r\n'
    client_socket.send(request.encode())

    # receive full response
    response = b''
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        response += chunk

    client_socket.close()

    # parse status line and headers
    if response:
        headers_part, body = response.split(b'\r\n\r\n', 1)
        headers_str = headers_part.decode('utf-8')
        header_lines = headers_str.split('\r\n')
        status_line = header_lines[0]

        # check status code
        if ' 200 ' in status_line:
            # get content-type from headers
            content_type = None
            for line in header_lines[1:]:
                if line.lower().startswith('content-type:'):
                    content_type = line.split(':', 1)[1].strip().lower()
                    break

            if content_type == 'text/html':
                # print body to console
                print(body.decode('utf-8', errors='ignore'))
            elif content_type in ['image/png', 'application/pdf']:
                # save file to save_directory
                file_name = os.path.basename(url_path)
                save_path = os.path.join(save_directory, file_name)
                with open(save_path, 'wb') as f:
                    f.write(body)
                print(f"Saved {file_name} to {save_path}")
            else:
                print("Unsupported content type")
        elif ' 404 ' in status_line:
            print("404 Not Found")
        else:
            print(f"Received status: {status_line}")
    else:
        print("No response received")

if __name__ == '__main__':
    main()

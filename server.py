import socket
import sys
import os
import urllib.parse
import time

def get_content_type(file_path):
    if file_path.endswith('.html'):
        return 'text/html'
    elif file_path.endswith('.png'):
        return 'image/png'
    elif file_path.endswith('.pdf'):
        return 'application/pdf'
    else:
        return None

def generate_404_html(requested_path):
    html = '<html><head><style>'
    html += 'body { font-family: Arial, sans-serif; text-align: center; color: #666; }'
    html += '.container { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }'
    html += '.big-404 { font-size: 120px; font-weight: bold; color: #ccc; }'
    html += '.message { font-size: 18px; margin: 20px 0; }'
    html += '.path { font-family: monospace; color: #999; }'
    html += '</style></head><body>'
    html += '<div class="container">'
    html += '<div class="big-404">404</div>'
    html += '<div class="message">Not Found</div>'
    html += f'<div class="path">The file "{requested_path}" could not be found.</div>'
    html += '</div></body></html>'
    return html

def handle_request(client_socket, directory):
    request = client_socket.recv(1024).decode('utf-8')
    if not request:
        return

    # Simulate 1-second processing delay
    time.sleep(1)

    # parse request to extract path
    request_line = request.split('\n')[0]
    parts = request_line.split()
    if len(parts) < 2 or parts[0] != 'GET':
        response = 'HTTP/1.1 400 Bad Request\r\n\r\n'.encode()
        client_socket.send(response)
        client_socket.close()
        return

    path = parts[1]
    # decode url encoding
    path = urllib.parse.unquote(path)
    # remove leading slash
    if path.startswith('/'):
        path = path[1:]

    file_path = os.path.join(directory, path)

    if os.path.isdir(file_path):
        # generate directory listing html
        # scan directory contents
        items = []
        try:
            for item in os.listdir(file_path):
                item_path = os.path.join(file_path, item)
                is_dir = os.path.isdir(item_path)
                size = os.path.getsize(item_path) if not is_dir else 0
                items.append((item, is_dir, size))
        except OSError:
            html = generate_404_html(path)
            response = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(html)}\r\n\r\n{html}'.encode()
            client_socket.send(response)
            client_socket.close()
            return

        # build simple html for directory listing
        title = path if path else 'Root'
        html = f'<html><head><meta charset="UTF-8"><title>Files in /{title}</title></head><body>\n'
        html += f'<h1>📁 Files in /{title}</h1>\n'
        html += '<ul>\n'
        if path and path != '/':
            # add parent directory link
            html += f'<li>🔙 <a href="../">../</a></li>\n'
        for item, is_dir, size in sorted(items):
            if is_dir:
                icon = '📁'
                rel_href = item + '/'
                display_name = item + '/'
            else:
                # determine icon based on file extension
                if item.endswith('.pdf'):
                    icon = '📕'
                elif item.endswith('.png') or item.endswith('.jpg'):
                    icon = '🖼️'
                elif item.endswith('.html'):
                    icon = '🌐'
                else:
                    icon = '📄'

                rel_href = item
                display_name = item

            html += f'<li>{icon} <a href="{rel_href}">{display_name}</a></li>\n'
        html += '</ul>\n</body></html>\n'

        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html)}\r\n\r\n{html}'
        client_socket.send(response.encode())
        client_socket.close()
        return

    if not os.path.isfile(file_path):
        html = generate_404_html(path)
        response = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(html)}\r\n\r\n{html}'.encode()
        client_socket.send(response)
        client_socket.close()
        return

    # check supported extensions
    content_type = get_content_type(file_path)
    if not content_type:
        html = generate_404_html(path)
        response = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(html)}\r\n\r\n{html}'.encode()
        client_socket.send(response)
        client_socket.close()
        return

    # build response with headers and content
    with open(file_path, 'rb') as f:
        content = f.read()
    response = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n'.encode() + content
    client_socket.send(response)
    client_socket.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python server.py <directory> [port]")
        sys.exit(1)

    directory = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    if not os.path.isdir(directory):
        print("Invalid directory")
        sys.exit(1)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(10)

    print(f"Serving directory: {directory} on http://127.0.0.1:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        handle_request(client_socket, directory)

if __name__ == '__main__':
    main()

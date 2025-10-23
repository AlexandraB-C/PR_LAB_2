import sys
import concurrent.futures
import socket

if len(sys.argv) < 3:
    host = 'localhost'
    port = 8080
    url_path = '/sample.pdf'
    num_requests = 50
else:
    host = sys.argv[1]
    port = int(sys.argv[2])
    if len(sys.argv) > 3:
        url_path = sys.argv[3]
    else:
        url_path = '/sample.pdf'
    if len(sys.argv) > 4:
        num_requests = int(sys.argv[4])
    else:
        num_requests = 50

def make_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    success = False
    try:
        client_socket.connect((host, port))
        request = f'GET {url_path} HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n'.encode()
        client_socket.send(request)
        # Receive full response
        response = b''
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk
        # Check if response contains HTTP/1.1 200 OK
        if b'HTTP/1.1 200 OK' in response:
            success = True
    except Exception:
        success = False
    finally:
        client_socket.close()
    return success

print(f"Sending {num_requests} concurrent requests to http://{host}:{port}{url_path}")

successful = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(make_request) for _ in range(num_requests)]
    # Wait for all to complete
    for future in concurrent.futures.as_completed(futures):
        if future.result():
            successful += 1

print(f"Requests sent: {num_requests}, Successful: {successful}, Failed: {num_requests - successful}")
print(f"Expected: {num_requests}, Actual: meh")

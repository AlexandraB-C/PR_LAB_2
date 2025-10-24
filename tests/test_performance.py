import sys
import time
import concurrent.futures
import socket

if len(sys.argv) != 3:
    print("Usage: python test_performance.py <host> <port>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

def make_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        request = b'GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n'
        client_socket.send(request)
        # receive full response
        response = b''
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk
    finally:
        client_socket.close()

start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(make_request) for _ in range(10)]
    # wait for all
    for future in concurrent.futures.as_completed(futures):
        future.result()  # exceptions

end_time = time.time()
total_time = end_time - start_time

print(f"Handled 10 concurrent requests in {total_time:.2f} seconds")

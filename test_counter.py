import socket
import threading
import time

def make_request(host, port, path):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        client_socket.sendall(request.encode())
        client_socket.recv(4096)
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

def test_counter(host, port, path, num_requests):
    threads = []
    start_time = time.time()
    
    for i in range(num_requests):
        thread = threading.Thread(target=make_request, args=(host, port, path))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    total_time = time.time() - start_time
    print(f"\nSent {num_requests} concurrent requests in {total_time:.2f} seconds")
    print(f"Now check the directory listing to see the hit count for {path}")
    print(f"Expected: {num_requests}, Actual: check in browser at http://{host}:{port}/")

if __name__ == "__main__":
    import sys
    
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    path = sys.argv[3] if len(sys.argv) > 3 else '/sample.pdf'
    num_requests = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    
    print(f"Testing counter on {host}:{port}{path} with {num_requests} requests")
    test_counter(host, port, path, num_requests)
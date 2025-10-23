import socket
import time
import sys

def make_request(host, port, path):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)
        client_socket.connect((host, port))
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        client_socket.sendall(request.encode())
        response = client_socket.recv(4096).decode('utf-8', errors='ignore')
        client_socket.close()
        
        if '200 OK' in response:
            return 200
        elif '429' in response:
            return 429
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

def main():
    rate = 5  # requests per second, default 5
    total_requests = 20
    server_host = 'localhost'
    server_port = 8080
    url_path = '/sample.pdf'

    if len(sys.argv) > 1:
        rate = float(sys.argv[1])
    if len(sys.argv) > 2:
        total_requests = int(sys.argv[2])
    if len(sys.argv) > 3:
        server_host = sys.argv[3]
    if len(sys.argv) > 4:
        server_port = int(sys.argv[4])
    if len(sys.argv) > 5:
        url_path = sys.argv[5]

    interval = 1.0 / rate if rate > 0 else 0

    print(f"Sending {total_requests} requests at {rate} req/sec to http://{server_host}:{server_port}{url_path}")
    
    start_time = time.time()
    successful = 0
    rate_limited = 0
    other_failed = 0

    for i in range(total_requests):
        req_start = time.time()
        status = make_request(server_host, server_port, url_path)
        req_end = time.time()
        
        if status == 200:
            successful += 1
        elif status == 429:
            rate_limited += 1
        else:
            other_failed += 1
        
        print(f"Request {i+1}: {status} ({req_end - req_start:.2f}s)")
        
        if i < total_requests - 1:  # no sleep after last
            time.sleep(interval)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n--- RESULTS ---")
    print(f"Total time: {total_time:.2f}s")
    print(f"Successful requests (200): {successful}")
    print(f"Rate limited (429): {rate_limited}")
    print(f"Other failed: {other_failed}")
    throughput = successful / total_time if total_time > 0 else 0
    print(f"Successful requests per second: {throughput:.2f}")

    expected_time = (total_requests - 1) * interval if total_requests > 0 else 0
    print(f"Expected time (sequential): {expected_time:.2f}s")

if __name__ == '__main__':
    main()
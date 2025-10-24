import sys
import time
import socket
import threading
import concurrent.futures

if len(sys.argv) < 3:
    mode = 'burst'  # 'burst' or 'sustained'
    total_requests = 20
    host = 'localhost'
    port = 8080
else:
    mode = sys.argv[1]  # 'burst' or 'sustained'
    total_requests = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    host = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 8080

def send_request(request_num):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    success_200 = False
    rate_limited_429 = False
    try:
        client_socket.settimeout(3)
        client_socket.connect((host, port))
        request = b'GET /sample.pdf HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n'
        client_socket.send(request)
        response = b''
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk
        if b'HTTP/1.1 200 OK' in response:
            success_200 = True
        elif b'HTTP/1.1 429 Too Many Requests' in response:
            rate_limited_429 = True
    except Exception as e:
        print(f"Request {request_num}: Connection error - {e}")
    finally:
        client_socket.close()
    return success_200, rate_limited_429

if mode == 'burst':
    print(f"🚀 BURST MODE: Sending {total_requests} requests simultaneously")
    print(f"Expected: ~5 successful (200), ~{total_requests - 5} rate-limited (429)\n")
    
    start_time = time.time()
    successful = 0
    rate_limited = 0
    
    # Send all requests concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=total_requests) as executor:
        futures = [executor.submit(send_request, i+1) for i in range(total_requests)]
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            success, limited = future.result()
            if success:
                successful += 1
                print(f"Request {i+1}: ✅ 200 OK")
            elif limited:
                rate_limited += 1
                print(f"Request {i+1}: ❌ 429 Too Many Requests")
            else:
                print(f"Request {i+1}: ⚠️ Failed")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n{'='*50}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Successful (200): {successful}")
    print(f"Rate limited (429): {rate_limited}")
    print(f"{'='*50}")

elif mode == 'sustained':
    rate_per_sec = 4  # Default: stay under the limit
    if len(sys.argv) > 5:
        rate_per_sec = float(sys.argv[5])
    
    print(f"⏱️  SUSTAINED MODE: Sending {total_requests} requests at {rate_per_sec} req/sec")
    print(f"Expected: All successful if rate <= 5 req/sec\n")
    
    interval = 1.0 / rate_per_sec if rate_per_sec > 0 else 0
    
    start_time = time.time()
    successful = 0
    rate_limited = 0
    
    for i in range(total_requests):
        success, limited = send_request(i+1)
        if success:
            successful += 1
            print(f"Request {i+1}: ✅ 200 OK")
        elif limited:
            rate_limited += 1
            print(f"Request {i+1}: ❌ 429 Too Many Requests")
        
        # Delay to maintain the specified rate
        if i < total_requests - 1:
            time.sleep(interval)
    
    end_time = time.time()
    total_time = end_time - start_time
    throughput = successful / total_time if total_time > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Successful (200): {successful}")
    print(f"Rate limited (429): {rate_limited}")
    print(f"Throughput: {throughput:.2f} successful req/sec")
    print(f"{'='*50}")

else:
    print("Invalid mode. Use 'burst' or 'sustained'")
    sys.exit(1)
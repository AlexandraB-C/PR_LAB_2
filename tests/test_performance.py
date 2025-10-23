import sys
import time
import concurrent.futures
import urllib.request

if len(sys.argv) != 3:
    print("Usage: python test_performance.py <host> <port>")
    sys.exit(1)

host = sys.argv[1]
port = sys.argv[2]
url = f"http://{host}:{port}/"

def make_request():
    with urllib.request.urlopen(url) as response:
        # Ensure the request completes
        pass

start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(make_request) for _ in range(10)]
    # Wait for all to complete
    for future in concurrent.futures.as_completed(futures):
        future.result()  # Raise any exceptions

end_time = time.time()
total_time = end_time - start_time

print(f"Handled 10 concurrent requests in {total_time:.2f} seconds")

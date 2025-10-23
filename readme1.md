# Lab 2: Concurrent HTTP Server

**Author: Bujor-Cobili Alexandra**

## Part 1: Performance Testing - Single-threaded Baseline

This section establishes the performance baseline for the single-threaded HTTP server.

**Commands run:**

1. Start the server:
   ```
   python server.py content 8080
   ```

2. Terminal output: "Serving directory: content on http://127.0.0.1:8080"

**Run the performance test:**

   ```
   python tests/test_performance.py localhost 8080
   ```

**Terminal output:**

   ```
   Handled 10 concurrent requests in 10.XX seconds
   ```

[SCREENSHOT 1: Terminal showing test output with ~10 seconds timing]

**Explanation:**
- The single-threaded server processes requests sequentially, with each request taking 1 second due to the added delay.
- Even though 10 requests are sent concurrently, they are queued and handled one by one.
- Therefore, total time ≈ 10 requests × 1 second = ~10 seconds.

## Part 2: Multi-threaded Server Implementation

**Commands run:**

1. Start the multi-threaded server:
   ```
   python server_multi.py content 8080
   ```

2. Terminal output: "Multi-threaded server serving directory: content on http://127.0.0.1:8080"

**Run the performance test:**

   ```
   python tests/test_performance.py localhost 8080
   ```

**Terminal output:**

   ```
   Handled 10 concurrent requests in 1.XX seconds
   ```

[SCREENSHOT 2: Terminal showing test output with ~1 second timing]

**Explanation:**
- Multi-threaded server processes requests in parallel using ThreadPoolExecutor with max_workers=10.
- 10 concurrent requests now take ~1 second (all processed simultaneously).

**Server logs output:**

   ```
   [Thread] Processing request for /
   [Thread] Processing request for /
   ...
   ```

[SCREENSHOT 3: Terminal showing thread names in server logs]

### Performance Comparison

| Server Type       | Time for 10 Requests | Explanation |
|-------------------|----------------------|-------------|
| Single-threaded   | ~10 seconds          | Sequential processing |
| Multi-threaded    | ~1 second            | Parallel processing   |

## Part 3: Counter Feature (2 points)

### 3.1 Naive Implementation - Race Condition Demo

This implementation intentionally creates a race condition by not using synchronization.

**Naive counter increment code:**

```python
# Increment hit counter (naive - no lock)
current = hits[file_path]
time.sleep(0.01)  # Force race condition
hits[file_path] = current + 1
```

**Commands run:**

1. Start the naive counter server:
   ```
   python server_naive.py content 8080
   ```

2. Terminal output: "Naive counter server serving directory: content on http://127.0.0.1:8080"

**Run the concurrent requests:**

   ```
   python tests/test_counter.py localhost 8080 /sample.pdf 50
   ```

**Terminal output:**

   ```
   Sending 50 concurrent requests to http://localhost:8080/sample.pdf
   Check browser at http://localhost:8080/ to see hit count
   Expected: 50, Actual: (check in browser)
   ```

[SCREENSHOT 5: Browser showing directory listing with INCORRECT hit count (less than 50)]

**Open browser to http://localhost:8080/ to see the directory listing with hit counts.**

**Expected result:** The hit count for sample.pdf should be significantly less than 50 (e.g., 30-45) due to the race condition.

[SCREENSHOT 6: Terminal showing "Expected: 50" message]

**Explanation:** Without synchronization, multiple threads read the same counter value simultaneously and write back incremented values, causing lost updates. This demonstrates a race condition where concurrent access to shared data leads to incorrect results.

### 3.2 Fixed Implementation - Thread-safe Counter

This implementation fixes the race condition using proper synchronization.

**Fixed counter increment code:**

```python
# Thread-safe counter increment
with lock:
    hits[file_path] += 1
```

**Commands run:**

1. Start the thread-safe server:
   ```
   python server_multi.py content 8080
   ```

2. Terminal output: "Multi-threaded server serving directory: content on http://127.0.0.1:8080"

**Run the concurrent requests:**

   ```
   python tests/test_counter.py localhost 8080 /sample.pdf 50
   ```

**Terminal output:**

   ```
   Sending 50 concurrent requests to http://localhost:8080/sample.pdf
   Requests sent: 50, Successful: 50, Failed: 0
   Check browser at http://localhost:8080/ to see hit count
   Expected: 50, Actual: (check in browser)
   ```

[SCREENSHOT 7: Browser showing directory listing with CORRECT hit count (exactly 50)]

**Open browser to http://localhost:8080/ to see the directory listing with hit counts.**

**Expected result:** The hit count for sample.pdf should be exactly 50.

**Explanation:** Using a lock ensures only one thread can increment the counter at a time. The hit count now matches the number of requests.

### Counter Implementation Comparison

| Implementation    | Expected | Actual | Race Condition? |
|-------------------|----------|--------|-----------------|
| Naive (no lock)   | 50       | ~35    | ✅ YES          |
| Fixed (lock)      | 50       | 50     | ❌ NO           |

## Part 4: Request Counter (with synchronization)

## Part 5: Rate Limiting by IP

## Part 6: Docker Configuration

The Docker setup containerizes the multi-threaded HTTP server for easy deployment.

**Dockerfile contents:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY server.py /app/
COPY server_multi.py /app/
COPY client.py /app/
COPY content /app/content/

EXPOSE 8080

CMD ["python", "server_multi.py", "content"]
```

**docker-compose.yml contents:**

```yaml
version: '3.8'

services:
  http-server:
    build: .
    command: python server_multi.py /app/content
    ports:
      - "8080:8080"
    volumes:
      - ./content:/app/content
```

## Run the containerized server:

   ```
   docker-compose up --build
   ```

**Terminal output:**

   ```
   Building http-server
   ...
   http-server_1  | Multi-threaded server serving directory: content on http://127.0.0.1:8080
   ```

[SCREENSHOT 6: Docker container running the multi-threaded server]

## Part 7: Testing with Friends

## Part 7: Testing with Friends

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

## Part 2: Multi-threaded Server

## Part 3: Request Counter (with race condition demonstration)

## Part 4: Request Counter (with synchronization)

## Part 5: Rate Limiting by IP

## Part 6: Docker Configuration

## Part 7: Testing with Friends

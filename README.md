# Lab 2: Concurrent HTTP Server

### Author: Bujor-Cobili Alexandra

## 1. Source Directory Structure
![ ](img/contents_root.png)

## Part 1: Performance Testing - Single-threaded Baseline

```
python server.py content 8080
python tests/test_performance.py localhost 8080
```

[SCREENSHOT 1: Terminal showing test output with ~10 seconds timing]

Single-threaded server processes requests sequentially, so 10 requests with 1s delay = ~10 seconds total

## 3. Multi-Threaded Server

```
python server_mult.py content 8080
python test_burst.py localhost 8080
```

Screenshot 2: Terminal showing ~1 second

Multi-threaded server handles all 10 requests concurrently. All finish around 1 second (the delay time), thus multi-threaded server is 10 times faster for concurrent requests.


## 4. Request Counter

### No Lock Implementation

```
python server_mult.py content 8080
python test_counter.py localhost 8080 /sample.pdf 50
```

### With Lock Implementation

```
python server_mult.py content 8080
python test_counter.py localhost 8080 /sample.pdf 50
```

## 5. Rate Limiting



## 5. Docker Configuration Files
![ ](img/docker.png)

Dockerfile contents

![ ](img/yml.png)

 docker-compose.yml contents

Dockerfile uses Python 3.11-slim base image, copies server.py, client.py, and content. docker-compose.yml defines http-server service with port mapping 8080:8080 and volume mount for live content updates.


## 8. Friends spam
During demo, I located friend's IP address using `ipconfig` or `ifconfig`, connected to their server IP on port 8080. 

![ ](img/friend_to_me.jpg)

I viewed their directory listings and downloaded files using my client: `python client.py <supposed_ip> 8080 /asd.pdf downloads/`.*

I swear it worked.

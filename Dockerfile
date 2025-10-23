FROM python:3.11-slim

WORKDIR /app

COPY server.py /app/
COPY server_mult.py /app/
COPY server_naive.py /app/
COPY client.py /app/
COPY test_burst.py /app/
COPY test_sustained.py /app/
COPY content /app/content/
COPY test_counter.py /app/

EXPOSE 8080

CMD ["python", "server_mult.py", "content"]
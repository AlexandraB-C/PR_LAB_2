FROM python:3.11-slim

WORKDIR /app

COPY server.py /app/
COPY server_multi.py /app/
COPY client.py /app/
COPY content /app/content/

EXPOSE 8080

CMD ["python", "server_multi.py", "content"]

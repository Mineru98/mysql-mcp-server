FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
COPY mysql_mcp_server/ .

RUN pip install -r requirements.txt 

COPY . .

EXPOSE 8081

CMD ["python", "mysql_mcp_server/main.py", "run"]

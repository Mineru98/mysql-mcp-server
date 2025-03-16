FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

EXPOSE 8081

CMD ["python", "mysql_mcp_server/main.py", "run"]

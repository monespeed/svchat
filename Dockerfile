FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN mkdir /app/server_files

EXPOSE 9090-9091

CMD ["python", "server.py"]
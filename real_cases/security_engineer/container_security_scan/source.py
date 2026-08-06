FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3 python3-pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
USER root
CMD ["python3", "app.py"]

# Hardcoded credentials in Dockerfile
ENV API_KEY="container_api_key_12345"
ENV DB_PASSWORD="container_db_password"
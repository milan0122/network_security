FROM python:3.11-slim-buster
WORKDIR /app
COPY . /app

RUN apt-get update -y && \
    apt-get install -y curl unzip && \
    pip install --no-cache-dir --upgrade pip && \
    pip install awscli && \
    pip install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /root/.cache

CMD ["python3","app.py"]
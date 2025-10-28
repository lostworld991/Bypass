FROM python:3.10-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN chmod 777 /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash", "start.sh"]

FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        build-essential \
        gcc \
        g++ \
        libffi-dev \
        libssl-dev \
        python3-dev \
        libleveldb-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/src/app

RUN chmod 777 /usr/src/app

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["bash", "start.sh"]

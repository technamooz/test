FROM python:3.11-slim

ARG XRAY_VERSION=1.8.24
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    XRAY_BINARY_PATH=/usr/local/bin/xray \
    XRAY_ENABLED=true \
    DATA_DIR=/data

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL "https://github.com/XTLS/Xray-core/releases/download/v${XRAY_VERSION}/Xray-linux-64.zip" -o /tmp/xray.zip \
    && unzip -p /tmp/xray.zip xray > /usr/local/bin/xray \
    && chmod 0755 /usr/local/bin/xray \
    && rm -f /tmp/xray.zip

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /data && chmod 0700 /data

EXPOSE 8080
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers --forwarded-allow-ips='*' --no-server-header"]

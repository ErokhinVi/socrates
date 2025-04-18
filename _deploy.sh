#!/bin/bash
set -e

APP_DIR=$1
REPO_URL=$2
OPENAI_API_KEY=$3
PORT=8000

# 1. Установка системных зависимостей
apt-get update
apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    ca-certificates \
    lsb-release \
    git \
    python3 \
    python3-venv \
    software-properties-common

# 2. Установка Nginx (mainline, последняя стабильная)
echo "deb http://nginx.org/packages/mainline/ubuntu $(lsb_release -cs) nginx" > /etc/apt/sources.list.d/nginx.list
curl -fsSL https://nginx.org/keys/nginx_signing.key | gpg --dearmor > /etc/apt/trusted.gpg.d/nginx.gpg
apt-get update
apt-get install -y nginx

# 3. Настройка firewall (если ufw установлен и активен)
if command -v ufw >/dev/null 2>&1; then
  if ufw status | grep -q inactive; then
    echo "ufw установлен, но не активен. Пропускаем настройку."
  else
    ufw allow 80/tcp || true
    ufw allow 443/tcp || true
  fi
fi

# 4. Клонирование репозитория
if [ -d "$APP_DIR" ]; then
  rm -rf $APP_DIR
fi
git clone $REPO_URL $APP_DIR || { echo "Ошибка клонирования репозитория"; exit 1; }
cd $APP_DIR

# 5. Создание виртуального окружения и установка зависимостей
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "PRODUCTION=true" > .env
echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env

# 6. Генерация self-signed SSL сертификата
mkdir -p /etc/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# 7. Конфигурирование Nginx
cp $APP_DIR/config/nginx-fastapi.conf /etc/nginx/conf.d/app.conf
nginx -t

# 8. Создание systemd unit-файла с Environment
cat > /etc/systemd/system/app.service << EOL
[Unit]
Description=FastAPI Application
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port $PORT
Environment=PRODUCTION=true
Environment=OPENAI_API_KEY=$OPENAI_API_KEY
Restart=always
ExecStartPre=/bin/mkdir -p $APP_DIR/tmp

[Install]
WantedBy=multi-user.target
EOL

# 9. Запуск сервисов
if lsof -ti:$PORT > /dev/null; then
  echo "Killing existing processes on port $PORT"
  lsof -ti:$PORT | xargs kill -9
fi
systemctl stop app.service || true
systemctl daemon-reload
systemctl enable app.service nginx
systemctl restart app.service nginx

# 10. Очистка
apt-get clean
rm -rf /var/lib/apt/lists/*

# 11. Финал
IP_ADDRESS=$(curl -s ifconfig.me)
echo "=== Deployment complete ==="
echo "Application URLs:"
echo "HTTP: http://$IP_ADDRESS"
echo "HTTPS: https://$IP_ADDRESS"
echo "API Docs: https://$IP_ADDRESS/docs"

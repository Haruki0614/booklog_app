# Dockerfile for Render deployment

FROM python:3.11-slim

# 環境変数設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /usr/src/app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコピーして依存関係をインストール
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY backend/ .

# 静的ファイルディレクトリを作成
RUN mkdir -p staticfiles

# ポートを公開
EXPOSE $PORT

# 起動スクリプトを作成
RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python manage.py collectstatic --noinput\n\
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT' > start.sh && \
chmod +x start.sh

# アプリケーションを起動
CMD ["./start.sh"]
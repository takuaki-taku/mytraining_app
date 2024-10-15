   # Dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt ./
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   # 環境変数を設定
   ENV FLASK_APP=run.py
   ENV FLASK_ENV=development


   # Flaskアプリをgunicornで起動
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
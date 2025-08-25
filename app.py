# app.py

import os
import threading
from flask import Flask
# Импортируем основную функцию из нашего скрипта бота
from bot import main as run_bot_main

# Создаем Flask-приложение
app = Flask(__name__)

@app.route('/health')
def health_check():
    """Эта страница нужна для 'пинга' сервисами мониторинга."""
    return {"status": "ok", "message": "Bot is running"}, 200

def start_bot_in_thread():
    """Запускает бота в отдельном потоке, чтобы не блокировать веб-сервер."""
    logger.info("Starting Telegram bot in a background thread...")
    bot_thread = threading.Thread(target=run_bot_main)
    bot_thread.daemon = True
    bot_thread.start()

if __name__ == "__main__":
    # Запускаем бота
    start_bot_in_thread()
    
    # Запускаем веб-сервер
    # Он будет использовать порт из переменной окружения PORT (для хостингов) или 5000 по умолчанию
    port = int(os.environ.get("PORT", 5000))
    print(f"Flask app starting on port {port}...")
    app.run(host='0.0.0.0', port=port)
import threading
import webview

from src.gui import create_app
from src.scanner import Scanner

if __name__ == '__main__':
    # Надстройки
    title = 'Arbitrage scanner'
    exchanges = ('bybit', 'mexc')
    # Бэкенд и фронтенд
    backend = Scanner(exchanges)
    frontend = create_app(title, backend.get_data)
    # Запуск
    thread = threading.Thread(target=backend.run_async)
    webview.create_window(title, frontend)
    thread.start()
    webview.start()
    # Ожидание завершения бэкенда
    thread.join()

from gui import create_app
from scanner import Scanner, thread_run
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == "__main__":
    # Исправление предупреждения об утечке семафоров в multiprocessing
    # Актуально только для debug-режима Flask.
    import multiprocessing

    multiprocessing.set_start_method('spawn', force=True)

    # Основная точка входа.
    scanner = Scanner()
    thread = thread_run(scanner)
    thread.start()
    app = create_app(scanner)
    app.run(debug=True)
    scanner.stop()
    thread.join()

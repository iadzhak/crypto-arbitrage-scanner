import asyncio
import logging
import threading

from src.gui import ScannerModel
from src.ccxt_utils import create_exchange, ccxt_available_exchanges

logger = logging.getLogger(__name__)


def thread_run(scanner):
    thread = threading.Thread(target=lambda: asyncio.run(scanner.run()))
    return thread


class Scanner(ScannerModel):
    def __init__(self):
        self.exchanges = {}
        self._loaded_exchanges = {ex: True for ex in ccxt_available_exchanges()}
        self.watchlist = []
        self._tasks = []
        self._stop = False
        self._load_status = 1
        self._load_status_lock = asyncio.Lock()

    def load_status(self) -> int:
        return self._load_status

    def loaded_exchanges(self) -> list[tuple[str, bool]]:
        return [(ex, s) for ex, s in self._loaded_exchanges.items()]

    def set_watchlist(self, watchlist) -> None:
        self.watchlist = watchlist

    def stop(self):
        self._stop = True

    async def run(self):
        tasks = [asyncio.create_task(self._load_exchange(ex)) for ex in self._loaded_exchanges.keys()]
        self._tasks.extend(tasks)
        while not self._stop:
            await asyncio.sleep(1)
        await self._close_tasks()
        await self._close_exchanges()

    async def _load_exchange(self, exchange_id: str):
        exchange = create_exchange(exchange_id)
        try:
            await exchange.load_markets()
            logger.info(f"{exchange_id} биржа загружена")
            self.exchanges[exchange_id] = exchange
            self._loaded_exchanges[exchange_id] = False
        except Exception as e:
            logger.info(f"{exchange_id} ошибка загрузки биржи {type(e)}")
            await exchange.close()
        except asyncio.CancelledError:
            await exchange.close()
        finally:
            async with self._load_status_lock:
                self._load_status += 1

    async def _close_tasks(self):
        for task in self._tasks:
            if not task.done():
                task.cancel()

    async def _close_exchanges(self):
        await asyncio.gather(*[exchange.close() for exchange in self.exchanges.values()])
        logger.info(f"Подключения к биржам закрыты")

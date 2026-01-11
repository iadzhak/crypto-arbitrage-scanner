import asyncio
import logging
import ccxt.async_support as ccxt

from .arbitrage_market import ArbitrageMarket

logger = logging.getLogger(__name__)


class Scanner:
    def __init__(self, exchanges):
        self.exchanges = {ex: getattr(ccxt, ex)() for ex in exchanges if ex in ccxt.exchanges}
        self._stop = False
        self._arbitrage = ArbitrageMarket()

    def get_data(self) -> list[dict]:
        return self._arbitrage.table

    def stop(self):
        self._stop = True

    async def run(self):
        # загрузить биржи
        await asyncio.gather(*[self._load_exchange(ex) for ex in self.exchanges.values()])
        # обновить данные в цикле
        while not self._stop:
            # обновить тикеры
            await asyncio.gather(*[self._update_tickers(ex) for ex in self.exchanges.values()])
            await asyncio.sleep(5)
        # закрыть подключения
        await asyncio.gather(*[ex.close() for ex in self.exchanges.values()])

    def run_async(self):
        asyncio.run(self.run())

    async def _load_exchange(self, exchange):
        try:
            await exchange.load_markets()
            self._arbitrage.generate_symbols(exchange)
        except Exception as e:
            logger.error(f"Ошибка загрузки биржи {exchange.name}: {e}")
            self.exchanges.pop(exchange.id)

    @staticmethod
    async def _update_tickers(exchange):
        try:
            for market in ('spot', 'swap'):
                tickers = await exchange.fetch_tickers(params={'type': market})
                exchange.tickers.update(tickers)
        except Exception as e:
            logger.error(f"Ошибка обновления тикеров {exchange.name}: {e}")

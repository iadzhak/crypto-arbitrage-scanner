import itertools
import ccxt.async_support as ccxt
from typing import Literal
from datetime import datetime

from .symbol import Symbol


class ArbitrageMarket(dict):

    def generate_symbols(self, exchange: ccxt.Exchange):
        for market in exchange.markets.values():
            if not market['active']:
                continue
            if market['type'] == 'spot':
                self._create_symbol(market['base'], market['quote'], exchange, 'spot')
            elif market['type'] == 'swap':
                if market['settle'] != market['quote']:
                    continue
                self._create_symbol(market['base'], market['quote'], exchange, 'swap')

    def _create_symbol(self, base: str, quote: str, exchange: ccxt.Exchange, market: Literal['spot', 'swap']):
        symbol = Symbol(base, quote)
        if symbol not in self:
            self[symbol] = {'spot': [], 'swap': []}
        self[symbol][market].append(exchange)

    @property
    def _spot_spot(self):
        """Генератор: (символ, генератор пар бирж (спот, спот))"""
        for symbol, markets in self.items():
            spot = markets['spot']
            if len(spot) >= 2:
                yield symbol, itertools.combinations(spot, 2)

    @property
    def _spot_swap(self):
        """Генератор: (символ, генератор пар бирж (спот, фьючерс))"""
        for symbol, markets in self.items():
            spot = markets['spot']
            swap = markets['swap']
            if spot and swap:
                yield symbol, itertools.product(spot, swap)

    @property
    def table_spot_spot(self):
        table = []
        for s, exchanges in self._spot_spot:
            for ex1, ex2 in exchanges:
                row = self.make_row(s.spot, s.spot, ex1, ex2)
                if not row:
                    continue
                row['type'] = 'spot-spot'
                table.append(row)
        return table

    @property
    def table_spot_swap(self):
        table = []
        for s, exchanges in self._spot_swap:
            for ex1, ex2 in exchanges:
                row = self.make_row(s.spot, s.swap, ex1, ex2)
                if not row:
                    continue
                row['type'] = 'spot-swap'
                table.append(row)
        return table

    @property
    def table(self):
        return self.table_spot_spot + self.table_spot_swap

    @staticmethod
    def make_row(s1, s2, ex1, ex2):
        # получаем тикеры
        ticker_1 = ex1.tickers.get(s1)
        ticker_2 = ex2.tickers.get(s2)
        if not (ticker_1 and ticker_2):
            return None
        # получаем цены bid, ask
        buy_1, sell_1 = ticker_1['ask'], ticker_1['bid']
        buy_2, sell_2 = ticker_2['ask'], ticker_2['bid']
        if not (buy_1 and sell_1 and buy_2 and sell_2):
            return None
        # получаем объемы
        vol_buy_1, vol_sell_1 = ticker_1['askVolume'], ticker_1['bidVolume']
        vol_buy_2, vol_sell_2 = ticker_2['askVolume'], ticker_2['bidVolume']
        volume = lambda b, s: min(b, s) if b and s else b or s
        margin = lambda b, s: round((s / b - 1) * 100, 2)
        # время последнего обновления
        t1 = ex1.lastRestRequestTimestamp / 1000
        t2 = ex2.lastRestRequestTimestamp / 1000
        updated = datetime.now() - datetime.fromtimestamp(min(t1, t2))
        # формируем строку
        row = {
            'updated': f'{updated.seconds} сек.',
            'ex1': ex1.id,
            'ex2': ex2.id,
            's1': s1,
            's2': s2,
            'buy_sell': margin(buy_1, sell_2),
            'vol_buy_sell': volume(vol_buy_1, vol_sell_2),
            'sell_buy': margin(buy_2, sell_1),
            'vol_sell_buy': volume(vol_buy_2, vol_sell_1),
        }

        return row

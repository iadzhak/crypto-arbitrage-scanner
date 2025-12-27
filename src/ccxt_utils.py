import ccxt.async_support as ccxt


def ccxt_available_exchanges(method: str = 'fetchTickers'):
    """Список доступных бирж с поддержкой метода, по умолчанию fetchTickers"""
    return [e for e in ccxt.exchanges if getattr(ccxt, e)().has[method] is True]


def create_exchange(exchange_name: str, max_retries: int = 2, delay: int = 1000):
    """Создание экземпляра биржи"""
    exchange = getattr(ccxt, exchange_name)()
    exchange.options['maxRetriesOnFailure'] = max_retries
    exchange.options['maxRetriesOnFailureDelay'] = delay
    return exchange

import pytest

from src.scanner.symbol import Symbol


@pytest.mark.parametrize('base, quote, spot, swap', [
    ('BTC', 'USDT', 'BTC/USDT', 'BTC/USDT:USDT'),
])
def test_symbol(base, quote, spot, swap):
    symbol = Symbol(base, quote)
    symbol2 = Symbol(base, quote)
    symbol3 = Symbol('lal', 'hhf')
    assert symbol.spot == spot and symbol.swap == swap
    assert symbol == symbol2 and symbol != symbol3

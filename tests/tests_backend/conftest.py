import pytest
import pytest_asyncio
import asyncio
from src.scanner import Scanner

SCANNER_PARAMS = [  # input, expected exchanges
    (('bybit', 'mexc'), ('bybit', 'mexc')),  # all_working
    (('lala', 'gaga'), tuple())  # all_not_working
]


@pytest.fixture(scope="session", params=SCANNER_PARAMS, ids=('all_working', 'all_not_working'))
def cxt(request):
    exchanges, expected = request.param
    scanner = Scanner(exchanges)
    return scanner, expected


@pytest_asyncio.fixture(scope='function')
async def scanner_stop(cxt):
    scanner, _ = cxt
    await asyncio.sleep(5)
    scanner.stop()

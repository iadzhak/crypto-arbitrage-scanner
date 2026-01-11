import pytest


@pytest.mark.asyncio
async def test_scanner(cxt, scanner_stop):
    scanner, expected = cxt
    assert len(scanner.exchanges) == len(expected), "Неправильно добавились биржи"

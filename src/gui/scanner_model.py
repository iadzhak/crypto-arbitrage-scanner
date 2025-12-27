from abc import ABC, abstractmethod


class ScannerModel(ABC):

    @abstractmethod
    def available_exchanges(self) -> tuple[str, bool]:
        """Список доступных бирж."""
        raise NotImplementedError

    @abstractmethod
    def set_watchlist(self, watchlist) -> None:
        """Установить список отслеживаемых бирж."""
        raise NotImplementedError

    @abstractmethod
    def load_status(self) -> int:
        """Текущий статус загрузки (количество проверенных бирж)"""
        raise NotImplementedError

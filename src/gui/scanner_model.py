from abc import ABC, abstractmethod


class ScannerModel(ABC):

    @abstractmethod
    def loaded_exchanges(self) -> list[tuple[str, bool]]:
        """Список загруженных бирж."""
        raise NotImplementedError

    @abstractmethod
    def set_watchlist(self, watchlist) -> None:
        """Установить список отслеживаемых бирж."""
        raise NotImplementedError

    @abstractmethod
    def load_status(self) -> int:
        """Текущий статус загрузки (количество проверенных бирж)"""
        raise NotImplementedError

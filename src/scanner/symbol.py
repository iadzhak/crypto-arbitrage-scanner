from dataclasses import dataclass


@dataclass
class Symbol:
    base: str
    quote: str

    def __eq__(self, other):
        if not isinstance(other, Symbol):
            return False
        return self.base == other.base and self.quote == other.quote

    def __hash__(self):
        return hash((self.base, self.quote))

    @property
    def spot(self):
        return f"{self.base}/{self.quote}"

    @property
    def swap(self):
        return f"{self.base}/{self.quote}:{self.quote}"

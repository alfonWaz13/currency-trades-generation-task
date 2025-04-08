from dataclasses import dataclass

@dataclass(frozen=True)
class CurrencyTradeId:
    value: str

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)

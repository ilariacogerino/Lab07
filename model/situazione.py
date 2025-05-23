import datetime
from dataclasses import dataclass


@dataclass
class Situazione:
    Localita: str
    Data: datetime.date
    Umidita: int

    def __eq__(self, other):
        return self.Localita == other.Localita and self.Data == other.Data

    def __hash__(self):
        return hash((self.Localita, self.Data))

    def __str__(self):
        return f"[{self.Localita} - {self.Data}] Umidità = {self.Umidita}"
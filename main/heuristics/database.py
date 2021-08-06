from typing import Dict

from django.db import connections
from main.heuristics.base import Heuristic


class DatabaseHeuristic(Heuristic):
    def __init__(self) -> None:
        super().__init__(
            name='Наличие в базах данных фишинговых сайтов',
            score=100,
            good='Не обнаружено',
            bad='Обнаружено',
        )

    def process(self, address: str) -> Dict[str, int]:
        domain = self.extract_domain(address)
        with connections['phishing'].cursor() as cursor:
            cursor.execute('SELECT domain FROM domains WHERE domain==%s', [domain])
            row = cursor.fetchone()
            self.phishing = row is not None
        return super().process(address)

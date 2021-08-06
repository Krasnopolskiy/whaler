from typing import Dict

from django.db import connections
from main.heuristics.base import Heuristic


class DatabaseHeuristic(Heuristic):
    def __init__(self) -> None:
        super().__init__(
            'Наличие в базах данных фишинговых сайтов',
            {
                'unknow': {'score': 0, 'comment': '', 'phishing': 0},
                'good': {'score': 0, 'comment': 'Не обнаружено', 'phishing': 0},
                'bad': {'score': 100, 'comment': 'Обнаружено', 'phishing': 2},
            }
        )

    def process(self, address: str) -> Dict[str, int]:
        domain = self.extract_domain(address)
        with connections['phishing'].cursor() as cursor:
            cursor.execute('SELECT domain FROM domains WHERE domain==%s', [domain])
            row = cursor.fetchone()
            self.result = self.conditions['good'] if row is None else self.conditions['bad']
        return super().process(address)

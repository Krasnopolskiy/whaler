from typing import Dict

from main.heuristics.ai.for_nn import make_prediction
from main.heuristics.base import Heuristic


class NeuroNetworkHeuristic(Heuristic):
    def __init__(self) -> None:
        super().__init__(
            'Оценка нейросети',
            {
                'good': {'score': 0, 'comment': 'Угроза не обнаружена', 'phishing': 0},
                'bad': {'score': 60, 'comment': 'Потенциальная угроза', 'phishing': 2},
            },
        )

    def process(self, address: str) -> Dict[str, int]:
        domain = self.extract_domain(address)
        malicious = make_prediction(domain)
        self.result = self.conditions['bad'] if malicious else self.conditions['good']
        return super().process(address)

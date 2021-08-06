from typing import Dict

from main.heuristics.ai.for_nn import make_prediction
from main.heuristics.base import Heuristic


class NeuroNetworkHeuristic(Heuristic):
    def __init__(self) -> None:
        super().__init__(
            'Оценка нейросети',
            {
                'good': {'score': 0, 'comment': 'Угроза не обнаружена', 'phishing': 0},
                'bad': {'score': 35, 'comment': 'Потенциальная угроза', 'phishing': 2},
            },
        )

    def process(self, address: str) -> Dict[str, int]:
        domain = self.extract_domain(address)
        is_good = make_prediction(domain)
        self.result = self.conditions['good'] if is_good else self.conditions['bad']
        return super().process(address)

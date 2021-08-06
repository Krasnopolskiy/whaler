from main.heuristics.base import Heuristic
from typing import Dict, List


class Checker:
    def __init__(self, heuristics: List[Heuristic]) -> None:
        self.heuristics: List[Heuristic] = [heuristic() for heuristic in heuristics]

    def process(self, address: str) -> Dict[str, int]:
        result = {'checks': [], 'overall': 0}
        for heuristic in self.heuristics:
            check = heuristic.process(address)
            result['checks'].append(check)
            result['overall'] = min(result['overall'] + check['result']['score'], 100)
        return result

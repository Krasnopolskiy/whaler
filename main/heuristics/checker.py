from main.heuristics.base import Heuristic
from typing import Dict, List


class Checker:
    def __init__(self, heuristics: List[Heuristic]) -> None:
        self.heuristics: List[Heuristic] = [heuristic() for heuristic in heuristics]

    def process(self, address: str) -> Dict[str, int]:
        result = dict()
        for heuristic in self.heuristics:
            result.update(heuristic.process(address))
        return result

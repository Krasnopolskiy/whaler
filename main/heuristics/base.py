from typing import Dict


class Heuristic:
    def __init__(self, name: str, score: int) -> None:
        self.name: str = name
        self.score: str = score
        self.phishing: bool = False

    def process(self, address: str) -> Dict[str, int]:
        return {self.name: self.score if self.phishing else 0}

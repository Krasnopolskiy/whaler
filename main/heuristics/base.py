from typing import Dict

from tldextract import extract


class Heuristic:
    def __init__(self, name, conditions) -> None:
        self.name: str = name
        self.conditions: Dict = conditions
        self.result: Dict = None

    def process(self, address: str) -> Dict[str, int]:
        return {'name': self.name, 'result': self.result}

    @staticmethod
    def extract_domain(address: str) -> str:
        address = extract(address)
        return '.'.join((address.domain, address.suffix))

from typing import Dict

from main.heuristics.base import Heuristic
from requests import post


class SafeBrowsingHeuristic(Heuristic):
    GOOGLE_API_KEY: str = 'AIzaSyChyY_0VLv6whc-OiTwkdJJS1n6KrvQIlI'

    def __init__(self, **kwargs) -> None:
        super().__init__(
            name='Google Safe Browsing',
            score=100,
            good='Не обнаружено',
            bad='Обнаружено',
        )

    def process(self, address: str) -> Dict[str, int]:
        domain = self.extract_domain(address)
        return super().process(address)

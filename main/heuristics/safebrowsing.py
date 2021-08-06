from typing import Dict

from main.heuristics.base import Heuristic
from pysafebrowsing import SafeBrowsing
from whaler.settings import GOOGLE_SAFE_BROWSING_KEY


class SafeBrowsingHeuristic(Heuristic):
    GOOGLE_API_KEY = GOOGLE_SAFE_BROWSING_KEY

    def __init__(self, **kwargs) -> None:
        super().__init__(
            'Google Safe Browsing',
            {
                'good': {'score': 0, 'comment': 'Не обнаружено', 'phishing': 0},
                'bad': {'score': 100, 'comment': 'Вредоносный', 'phishing': 2},
            }
        )

    def process(self, address: str) -> Dict[str, int]:
        domain = self.extract_domain(address)
        api = SafeBrowsing(self.GOOGLE_API_KEY)
        malicious = api.lookup_url(domain)['malicious']
        self.result = self.conditions['bad'] if malicious else self.conditions['good']
        return super().process(address)

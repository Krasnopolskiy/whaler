from typing import Dict

from main.heuristics.base import Heuristic
from pysafebrowsing import SafeBrowsing
from whaler.settings import YANDEX_SAFE_BROWSING_KEY


class YandexSafeBrowsingHeuristic(Heuristic):
    def __init__(self) -> None:
        super().__init__(
            'Yandex Safe Browsing',
            {
                'good': {'score': 0, 'comment': 'Не обнаружено', 'phishing': 0},
                'bad': {'score': 100, 'comment': 'Вредоносный', 'phishing': 2},
            },
        )

    def process(self, address: str) -> Dict[str, int]:
        domain = self.extract_domain(address)
        api = SafeBrowsing(
            YANDEX_SAFE_BROWSING_KEY,
            api_url='https://sba.yandex.net/v4/threatMatches:find',
        )
        malicious = api.lookup_url(domain)['malicious']
        self.result = self.conditions['bad'] if malicious else self.conditions['good']
        return super().process(address)

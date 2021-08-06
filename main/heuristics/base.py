from typing import Dict


class Heuristic:
    def __init__(self, **kwargs) -> None:
        for key in ('name', 'score', 'good', 'bad'):
            setattr(self, key, kwargs.get(key))
        self.phishing: bool = False

    def process(self, address: str) -> Dict[str, int]:
        return {
            'name': self.name,
            'result': {'phishing': True, 'comment': self.bad, 'score': self.score}
            if self.phishing
            else {'phishing': False, 'comment': self.good, 'score': 0},
        }

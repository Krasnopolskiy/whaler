from socket import socket
from ssl import create_default_context
from typing import Dict

from main.heuristics.base import Heuristic


class CertificateHeuristic(Heuristic):
    ISSUERS = ['R3', 'ZeroSSL RSA Domain Secure Site CA']

    def __init__(self) -> None:
        super().__init__(
            'Сертификат',
            {
                'unknown': {'score': 15, 'comment': 'Не обнаружен', 'phishing': 2},
                'good': {
                    'score': 0,
                    'comment': 'Действительный сертификат',
                    'phishing': 0,
                },
                'bad': {
                    'score': 10,
                    'comment': 'Самоподписанный сертификат',
                    'phishing': 1,
                },
            },
        )

    def process(self, address: str) -> Dict[str, int]:
        domain = self.extract_domain(address)
        try:
            issuer = self.get_cert_info(domain)
            self.result = (
                self.conditions['bad']
                if issuer in self.ISSUERS
                else self.conditions['good']
            )
        except:
            self.result = self.conditions['unknown']
        return super().process(address)

    def get_cert_info(self, host: str, port=443):
        ctx = create_default_context()
        with ctx.wrap_socket(socket(), server_hostname=host) as sock:
            sock.connect((host, port))
            cert = sock.getpeercert()
        issuer = dict(x[0] for x in cert['issuer'])
        return issuer

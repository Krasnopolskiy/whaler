import socket
import ssl
from typing import Dict

from main.heuristics.base import Heuristic
from tldextract import extract


class CertificateHeuristic(Heuristic):
    def __init__(self) -> None:
        super().__init__(
            name="Рейтинг сертификата",
            score=100,
            good="Нет подозрений",
            bad="Есть подозрения",
        )

    def process(self, address: str) -> Dict[str, int]:
        address = extract(address)
        domain = ".".join((address.domain, address.suffix))

        self.score = self.get_cert_rate(domain)
        self.phishing = self.score > 0

        return super().process(address)

    def get_cert_info(self, host: str, port=443):
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.connect((host, port))
            cert = s.getpeercert()

        subject = dict(x[0] for x in cert["subject"])
        issuer = dict(x[0] for x in cert["issuer"])

        return subject, issuer

    def get_cert_rate(self, host):
        _, issuer = self.get_cert_info(host)
        rate = issuer.get("commonName", 0)
        return rate

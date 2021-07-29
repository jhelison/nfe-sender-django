from packages.core.certificate import CertificateA1
from packages.core.sefaz_client import SefazClient
from packages.core.sefaz_requests import SefazRequest


def process_status(data):
    cert = CertificateA1(data["certificate"], data["password"])
    url, service, root = SefazRequest().status_servico()

    return SefazRequest.response_to_dict(SefazClient(cert).post(url, service, root))

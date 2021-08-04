from packages.core.certificate import CertificateA1
from packages.core.sefaz_client import SefazClient
from packages.core.sefaz_requests import SefazRequest


def process_status(
    base64_certificate: str, certificate_password: str, is_hom: bool = True
) -> dict:
    cert = CertificateA1(base64_certificate, certificate_password)
    url, service, root = SefazRequest(is_hom=is_hom).status_servico()

    return SefazRequest.response_to_dict(SefazClient(cert).post(url, service, root))


def process_consulta_protocolo(
    base64_certificate: str,
    certificate_password: str,
    chNFe: str,
    is_hom: bool = True,
):
    cert = CertificateA1(base64_certificate, certificate_password)
    url, service, root = SefazRequest(is_hom=is_hom).consulta_protocolo(chNFe)

    return SefazRequest.response_to_dict(SefazClient(cert).post(url, service, root))

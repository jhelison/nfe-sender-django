from .certificate import CertificateA1
from .sefaz_client import SefazClient
from .sefaz_requests import SefazRequest
from .signer import Signer

from lxml import etree

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
) -> dict:
    cert = CertificateA1(base64_certificate, certificate_password)
    url, service, root = SefazRequest(is_hom=is_hom).consulta_protocolo(chNFe)

    return SefazRequest.response_to_dict(SefazClient(cert).post(url, service, root))

def process_autorizacao(
    base64_certificate: str,
    certificate_password: str,
    NFe: str,
    is_hom: bool = True,
) -> dict:
    cert = CertificateA1(base64_certificate, certificate_password)
    signer = Signer(cert)
    signed_xml = signer.sign_nfe(NFe)
    
    url, service, root = SefazRequest(is_hom=is_hom).autorizacao(signed_xml)
    
    return etree.tostring(root).decode()
    
    
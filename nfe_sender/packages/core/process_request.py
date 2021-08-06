from .certificate import CertificateA1
from .sefaz_client import SefazClient
from .sefaz_requests import SefazRequest
from .signer import Signer

from .xml_parser import XMLParser

from lxml import etree


def process_status(user_data: dict) -> dict:
    cert = CertificateA1(
        user_data["base64_certificate"], user_data["certificate_password"]
    )
    url, service, root = SefazRequest(is_hom=user_data["is_hom"]).status_servico()

    reponse = XMLParser((SefazClient(cert).post(url, service, root)))

    return reponse.dict


def process_consulta_protocolo(user_data: dict, chNFe: str) -> dict:
    cert = CertificateA1(
        user_data["base64_certificate"], user_data["certificate_password"]
    )
    url, service, root = SefazRequest(is_hom=user_data["is_hom"]).consulta_protocolo(
        chNFe
    )

    reponse = XMLParser((SefazClient(cert).post(url, service, root)))

    return reponse.dict


def process_autorizacao(
    base64_certificate: str,
    certificate_password: str,
    xml: str,
    is_hom: bool = True,
) -> dict:
    cert = CertificateA1(base64_certificate, certificate_password)
    signer = Signer(cert, is_hom=is_hom)
    signed_xml = signer.sign_xml(xml=xml)

    url, service, root = SefazRequest(is_hom=is_hom).autorizacao(signed_xml)

    response = SefazRequest.response_to_dict(SefazClient(cert).post(url, service, root))

    return response


def process_cancelamento(
    base64_certificate: str,
    certificate_password: str,
    xml: str,
    is_hom: bool = True,
) -> dict:
    cert = CertificateA1(base64_certificate, certificate_password)
    signer = Signer(cert, is_hom=is_hom)
    signed_xml = signer.sign_xml(xml=xml)

    url, service, root = SefazRequest(is_hom=is_hom).cancelamento(signed_xml)

    # response = SefazRequest.response_to_dict(SefazClient(cert).post(url, service, root))

    return etree.tostring(root)

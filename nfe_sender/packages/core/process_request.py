from .certificate import CertificateA1
from .sefaz_client import SefazClient
from .sefaz_requests import SefazRequest

from .xml_parser import XMLParser, NFeParser, CancelamentoParser


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


def process_autorizacao(user_data: dict, xml: str) -> dict:
    cert = CertificateA1(
        user_data["base64_certificate"], user_data["certificate_password"]
    )

    nfe = NFeParser(xml)
    if user_data["is_hom"]:
        nfe.set_as_hom()
    nfe.sign(cert)

    url, service, root = SefazRequest(is_hom=user_data["is_hom"]).autorizacao(nfe.root)
    response = XMLParser(SefazClient(cert).post(url, service, root))

    return response.dict


def process_cancelamento(user_data: dict, xml: str) -> dict:
    cert = CertificateA1(
        user_data["base64_certificate"], user_data["certificate_password"]
    )

    canc = CancelamentoParser(xml)

    url, service, root, evento = SefazRequest(is_hom=user_data["is_hom"]).cancelamento(
        canc=canc, user_data=user_data
    )

    evento = XMLParser(evento)
    if user_data["is_hom"]:
        evento.set_as_hom()
    evento.sign(cert)

    root.append(evento.root)

    root = XMLParser(root)

    response = XMLParser(SefazClient(cert).post(url, service, root.root))

    return response.dict

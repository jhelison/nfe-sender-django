from lxml import etree
import time

from packages.core.xml_parser import el_with_text


class SefazRequest:
    """
    Build the xml to make some sefaz requests.

    Hom can be passed if the server will run as Homologação, it is defalt as true.
    """

    nsmap = {None: "http://www.portalfiscal.inf.br/nfe"}
    versao = "4.00"

    def __init__(self, is_hom: bool = True, cUF: int = 21) -> None:
        self.is_hom = is_hom
        self.cUF = cUF

    def status_servico(self) -> list:
        """
        Return Sefaz servies status.
        """
        URL = "https://{}sefazvirtual.fazenda.gov.br/NFeStatusServico4/NFeStatusServico4.asmx?wsdl".format(
            "hom." if self.is_hom else ""
        )
        SERVICE = "nfeStatusServicoNF"

        root = etree.Element("consStatServ", nsmap=self.nsmap, versao=self.versao)

        root.append(el_with_text("tpAmb", 2 if self.is_hom else 1))
        root.append(el_with_text("cUF", self.cUF))
        root.append(el_with_text("xServ", "STATUS"))

        return (URL, SERVICE, root)

    def consulta_protocolo(self, chNFe: str) -> list:
        """
        Returns the status of the set chNFe
        """

        URL = "https://{}sefazvirtual.fazenda.gov.br/NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx?wsdl".format(
            "hom." if self.is_hom else ""
        )
        SERVICE = "nfeConsultaNF"

        root = etree.Element("consSitNFe", nsmap=self.nsmap, versao=self.versao)

        root.append(el_with_text("tpAmb", 2 if self.is_hom else 1))
        root.append(el_with_text("xServ", "CONSULTAR"))
        root.append(el_with_text("chNFe", chNFe))

        return (URL, SERVICE, root)

    def autorizacao(self, xml: etree.Element) -> list:
        """
        Return the URl, service name and etree to send a NFe
        """

        URL = "https://{}sefazvirtual.fazenda.gov.br/NFeAutorizacao4/NFeAutorizacao4.asmx?wsdl".format(
            "hom." if self.is_hom else ""
        )
        SERVICE = "nfeAutorizacaoLote"

        root = etree.Element("enviNFe", nsmap=self.nsmap, versao=self.versao)

        root.append(el_with_text("idLote", str(int(time.time()))))
        root.append(el_with_text("indSinc", 1))

        root.append(xml)

        return (URL, SERVICE, root)

    def recepcao_evento(self, evento: etree.Element) -> list:
        URL = "https://{}sefazvirtual.fazenda.gov.br/NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx?wsdl".format(
            "hom." if self.is_hom else ""
        )
        SERVICE = "nfeRecepcaoEvento"

        root = etree.Element("envEvento", nsmap=self.nsmap, versao="1.00")
        root.append(el_with_text("idLote", str(int(time.time()))))
        root.append(evento)

        return URL, SERVICE, root

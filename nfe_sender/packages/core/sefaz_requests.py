from lxml import etree
import time
from datetime import datetime

from packages.core.xml_parser import CancelamentoParser


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

        root.append(self._element_with_text("tpAmb", 2 if self.is_hom else 1))
        root.append(self._element_with_text("cUF", self.cUF))
        root.append(self._element_with_text("xServ", "STATUS"))

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

        root.append(self._element_with_text("tpAmb", 2 if self.is_hom else 1))
        root.append(self._element_with_text("xServ", "CONSULTAR"))
        root.append(self._element_with_text("chNFe", chNFe))

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

        root.append(self._element_with_text("idLote", str(int(time.time()))))
        root.append(self._element_with_text("indSinc", 1))

        root.append(xml)

        return (URL, SERVICE, root)

    def cancelamento(self, canc: CancelamentoParser, user_data: dict) -> list:
        """
        Return the URl, service name and etree to cancel a NFe
        """

        URL = "https://{}sefazvirtual.fazenda.gov.br/NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx?wsdl".format(
            "hom." if self.is_hom else ""
        )
        SERVICE = "nfeRecepcaoEvento"

        root = etree.Element("envEvento", nsmap=self.nsmap, versao="1.00")
        root.append(self._element_with_text("idLote", str(int(time.time()))))

        evento = etree.Element("evento", nsmap=self.nsmap, versao="1.00")
        infEvento = etree.Element("infEvento", Id="ID" + "110111" + canc.chNFe + "01")
        infEvento.append(
            self._element_with_text(
                "cOrgao", user_data["uf"] if user_data["uf"] else 21
            )
        )
        infEvento.append(
            self._element_with_text("tpAmb", 2 if user_data["is_hom"] else 1)
        )
        infEvento.append(self._element_with_text("CNPJ", user_data["username"]))
        infEvento.append(self._element_with_text("chNFe", canc.chNFe))
        infEvento.append(
            self._element_with_text(
                "dhEvento", datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S-03:00")
            )
        )
        infEvento.append(self._element_with_text("tpEvento", "110111"))
        infEvento.append(self._element_with_text("nSeqEvento", "1"))
        infEvento.append(self._element_with_text("verEvento", "1.00"))
        detEvento = etree.Element("detEvento", versao="1.00")
        detEvento.append(self._element_with_text("descEvento", "Cancelamento"))
        detEvento.append(self._element_with_text("nProt", canc.nProt))
        detEvento.append(self._element_with_text("xJust", canc.xJust))
        infEvento.append(detEvento)
        evento.append(infEvento)

        return URL, SERVICE, root, evento

    @staticmethod
    def _element_with_text(tag: str, text: any) -> etree.Element:
        """
        Returns a etree element with a set tag and text inside
        """
        el = etree.Element(tag)
        el.text = str(text)

        return el

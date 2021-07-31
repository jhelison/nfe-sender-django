from lxml import etree


class SefazRequest:
    """
    Build the xml to make some sefaz requests.

    Hom can be passed if the server will run as Homologação, it is defalt as true.
    """

    nsmap = {None: "http://www.portalfiscal.inf.br/nfe"}

    def __init__(self, hom: bool = True, cUF: int = 21) -> None:
        self.hom = hom
        self.cUF = cUF

    def status_servico(self) -> dict:
        """
        Return Sefaz servies status.
        """
        URL = "https://{}sefazvirtual.fazenda.gov.br/NFeStatusServico4/NFeStatusServico4.asmx?wsdl".format(
            "hom." if self.hom else ""
        )
        SERVICE = "nfeStatusServicoNF"

        root = etree.Element("consStatServ", nsmap=self.nsmap, versao="4.00")

        root.append(self._element_with_text("tpAmb", 2 if self.hom else 1))
        root.append(self._element_with_text("cUF", self.cUF))
        root.append(self._element_with_text("xServ", "STATUS"))

        return (URL, SERVICE, root)

    def consulta_protocolo(self, chNFe: str) -> dict:
        """
        Returns the status of the set chNFe
        """

        URL = "https://{}sefazvirtual.fazenda.gov.br/NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx?wsdl".format(
            "hom." if self.hom else ""
        )
        SERVICE = "nfeConsultaNF"

        nsmap = {None: "http://www.portalfiscal.inf.br/nfe"}
        root = etree.Element("consSitNFe", nsmap=self.nsmap, versao="4.00")

        root.append(self._element_with_text("tpAmb", 2 if self.hom else 1))
        root.append(self._element_with_text("xServ", "CONSULTAR"))
        root.append(self._element_with_text("chNFe", chNFe))

        return (URL, SERVICE, root)

    @staticmethod
    def _element_with_text(tag: str, text: any) -> etree.Element:
        """
        Returns a etree element with a set tag and text inside
        """
        el = etree.Element(tag)
        el.text = str(text)

        return el

    @staticmethod
    def response_to_dict(root: etree.Element) -> dict:
        """
        Tranform the childs of the root lxml in a dict, mantaining the structure of their childs.
        """
        child_dict = {}

        for child in root:
            child_dict[etree.QName(child).localname] = child.text

        return child_dict
from copy import deepcopy
from lxml import etree
from .signer import Signer, CertificateA1
import xmltodict
from json import loads, dumps
import re


class XMLParser:

    root: etree.Element

    def __init__(self, xml: str) -> None:
        xml_no_meta = self._remove_metatag(xml)
        self.root = etree.fromstring(xml_no_meta)

    def remove_signature(self):
        for child in self.root.iter("*"):
            if child.tag.endswith("Signature"):
                self.root.remove(child)
                return

    def root_to_dict(self):
        xparsed = xmltodict.parse(etree.tostring(self.root))
        return loads(dumps(xparsed))
    
    def set_as_hom(self) -> None:
        root = deepcopy(self.root)

        for child in root.iter(r"{http://www.portalfiscal.inf.br/nfe}tpAmb"):
            child.text = "2"

        for child in root.iter(r"{http://www.portalfiscal.inf.br/nfe}dest"):
            for grandchild in child.iter(r"{http://www.portalfiscal.inf.br/nfe}xNome"):
                grandchild.text = (
                    "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"
                )

        self.root = root
        
    def sign(self, certificate: CertificateA1) -> None:
        self.remove_signature()
        
        self.root = Signer(certificate).sign_xml(self.root, self.uri)
        
        
    
    @property
    def uri():
        raise NotImplementedError

    @staticmethod
    def _remove_metatag(xml: str) -> str:
        return re.sub(r"<\?xml([\s\S]*?)\?>", "", xml)

    def __repr__(self) -> str:
        return etree.tostring(self.root).decode()


class NFeParser(XMLParser):
    def __init__(self, xml: str) -> None:
        super().__init__(xml)
        self._clean_nfe_tree()

    @property
    def uri(self):
        for child in self.root.iter("*"):
            if child.tag.endswith("infNFe"):
                return child.get("Id")
        return None

    def _clean_nfe_tree(self):
        xml_tree = deepcopy(self.root)
        nsmap = {None: "http://www.portalfiscal.inf.br/nfe"}
        NFe_root = etree.Element("NFe", nsmap=nsmap)

        for child in xml_tree:
            NFe_root.append(child)

        for child in NFe_root.iter("*"):
            if child.text is not None and not child.text.strip():
                child.text = None

        self.root = NFe_root


class CancelamentoParser(XMLParser):
    def __init__(self, xml: str) -> None:
        super().__init__(xml)

    @property
    def uri(self):
        for child in self.root.iter("*"):
            if child.tag.endswith("infCanc"):
                return child.get("Id")
        return None

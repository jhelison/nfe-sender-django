from copy import deepcopy
from typing import Union
from lxml import etree
from .signer import Signer, CertificateA1
import xmltodict
from json import loads, dumps
import re


class XMLParser:

    root: etree.Element

    def __init__(self, xml: Union[str, etree.Element]) -> None:
        if isinstance(xml, str):
            xml_no_meta = self._remove_metatag(xml)
            self.root = etree.fromstring(xml_no_meta)
        else:
            self.root = xml

    def remove_signature(self):
        for child in self.root.iter("*"):
            if etree.QName(child).localname == "Signature":
                self.root.remove(child)
                return

    def set_as_hom(self) -> None:
        root = deepcopy(self.root)

        for child in root.iter("*"):
            if etree.QName(child).localname == "tpAmb":
                child.text = "2"
                break

        for child in root.iter("*"):
            if etree.QName(child).localname == "dest":
                for grandchild in child.iter("*"):
                    if etree.QName(grandchild).localname == "xNome":
                        grandchild.text = (
                            "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"
                        )
                        break

        self.root = root

    def sign(self, certificate: CertificateA1) -> None:
        self.remove_signature()

        self.root = Signer(certificate).sign_xml(self.root, self.uri)

    @property
    def uri(self):
        for child in self.root.iter("*"):
            if child.get("Id"):
                return child.get("Id")
        return None

    @property
    def dict(self):
        root = deepcopy(self.root)

        for child in root.getiterator():
            child.tag = etree.QName(child).localname
        etree.cleanup_namespaces(root)

        xparsed = xmltodict.parse(etree.tostring(root))

        return loads(dumps(xparsed))

    @staticmethod
    def _remove_metatag(xml: str) -> str:
        return re.sub(r"<\?xml([\s\S]*?)\?>", "", xml)

    def __repr__(self) -> str:
        return etree.tostring(self.root).decode()


class NFeParser(XMLParser):
    def __init__(self, xml: str) -> None:
        super().__init__(xml)
        self._clean_nfe_tree()

    def _clean_nfe_tree(self) -> None:
        xml_tree = deepcopy(self.root)
        nsmap = {None: "http://www.portalfiscal.inf.br/nfe"}
        NFe_root = etree.Element("NFe", nsmap=nsmap)

        for child in xml_tree:
            NFe_root.append(child)

        for child in NFe_root.iter("*"):
            if child.text is not None and not child.text.strip():
                child.text = None

        self.root = NFe_root

    @property
    def is_valid(self) -> bool:
        return etree.QName(self.root).localname == "NFe"


class CancelamentoParser(XMLParser):
    def __init__(self, xml: str) -> None:
        super().__init__(xml)

    @property
    def is_valid(self) -> bool:
        return etree.QName(self.root).localname == "cancNFe"

    @property
    def chNFe(self) -> str:
        for child in self.root.iter("*"):
            if etree.QName(child).localname == "chNFe":
                return child.text
        return None

    @property
    def nProt(self) -> str:
        for child in self.root.iter("*"):
            if etree.QName(child).localname == "nProt":
                return child.text
        return None

    @property
    def xJust(self) -> str:
        for child in self.root.iter("*"):
            if etree.QName(child).localname == "xJust":
                return child.text
        return None

from packages.core.certificate import CertificateA1
from copy import deepcopy
from lxml import etree
import signxml


class Signer:
    """Signs a xml file and returns it as a Etree file"""

    def __init__(self, certificate: CertificateA1) -> None:
        self.certificate = certificate
        self.cert = certificate._certificate
        self.private_key = certificate._private_key
        self.password = certificate._password

    def sign_nfe(self, xml_element: etree.Element) -> etree.Element:
        clean_tree = self.clean_nfe_tree(xml_element)

        signer = signxml.XMLSigner(
            method=signxml.methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm="sha1",
            c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
        )
        signer.namespaces = {None: signer.namespaces["ds"]}

        signed_root = signer.sign(
            clean_tree,
            key=self.certificate.key,
            cert=self.cert,
            reference_uri=self.get_uri(clean_tree),
        )

        return signed_root

    @staticmethod
    def clean_nfe_tree(xml_tree: etree.Element) -> etree.Element:
        xml_tree = deepcopy(xml_tree)
        nsmap = {None: "http://www.portalfiscal.inf.br/nfe"}
        NFe_root = etree.Element("NFe", nsmap=nsmap)

        for child in xml_tree:
            if "infNFe" in str(child.tag):
                NFe_root.append(child)
                break

        for element in NFe_root.iter("*"):
            if element.text is not None and not element.text.strip():
                element.text = None

        return NFe_root

    @staticmethod
    def get_uri(xml_tree: etree.Element) -> str:
        for element in xml_tree.iter("*"):
            if "infNFe" in str(element.tag):
                return element.get("Id")
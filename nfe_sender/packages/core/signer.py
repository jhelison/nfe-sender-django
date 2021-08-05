from packages.core.certificate import CertificateA1
from copy import deepcopy
from lxml import etree
import signxml
import re

class Signer:
    """Signs a xml file and returns it as a Etree file"""

    def __init__(self, certificate: CertificateA1, is_hom:bool = True) -> None:
        self.certificate = certificate
        self.cert = certificate._certificate
        self.private_key = certificate._private_key
        self.password = certificate._password
        
        self.is_hom = is_hom

    def sign_xml(self, xml: str) -> etree.Element:
        clean_tree = self.clean_xml(xml)

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
            reference_uri=self._get_uri(clean_tree),
        )

        return signed_root
    
    def clean_xml(self, xml: str) -> etree.Element:
        #Remove xml meta tag
        xml_no_meta = re.sub('<\?xml([\s\S]*?)\?>', '', xml)
        xml_element = etree.fromstring(xml_no_meta)
        
        xml_element = self.set_as_hom(xml_element)
        xml_element = self.remove_signature(xml_element)
        
        if self.is_nfe(xml_element):
            xml_element = self.clean_nfe_tree(xml_element)
            
        return xml_element
        

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
    def _get_uri(xml_tree: etree.Element) -> str:
        for element in xml_tree.iter("*"):
            if "infNFe" in str(element.tag):
                return element.get("Id")
            if "infCanc" in str(element.tag):
                return element.get("Id")

    @staticmethod
    def remove_signature(xml_tree: etree.Element) -> etree.Element:
        root = deepcopy(xml_tree)
        
        for child in root:
            if child.tag.endswith('Signature'):
                root.remove(child)
                
        return root
    
    @staticmethod
    def set_as_hom(xml_tree: etree.Element) -> etree.Element:
        root = deepcopy(xml_tree)
        
        for child in root.iter(r'{http://www.portalfiscal.inf.br/nfe}tpAmb'):
            child.text = "2"
            
        for child in root.iter(r'{http://www.portalfiscal.inf.br/nfe}dest'):
            for grandchild in child.iter(r'{http://www.portalfiscal.inf.br/nfe}xNome'):
                grandchild.text = "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"
        
        
        return root
    
    @staticmethod
    def is_nfe(xml_tree: etree.Element) -> bool:
        return xml_tree.tag == "{http://www.portalfiscal.inf.br/nfe}NFe"
            
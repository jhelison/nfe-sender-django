from packages.core.certificate import CertificateA1
from lxml import etree
import signxml


class Signer:
    """Signs a xml file and returns it as a Etree file"""

    def __init__(self, certificate: CertificateA1) -> None:
        self.certificate = certificate
        self.cert = certificate._certificate
        self.private_key = certificate._private_key
        self.password = certificate._password

    def sign_xml(self, xml: etree.Element, uri: str) -> etree.Element:

        signer = signxml.XMLSigner(
            method=signxml.methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm="sha1",
            c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
        )
        signer.namespaces = {None: signer.namespaces["ds"]}

        signed_root = signer.sign(
            xml,
            key=self.certificate.key,
            cert=self.cert,
            reference_uri=uri,
        )

        return signed_root

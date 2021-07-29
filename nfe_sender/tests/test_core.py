from packages.core.certificate import CertificateA1
from packages.core.sefaz_requests import SefazRequest
from lxml import etree


def get_cert_base64():
    with open("./nfe_sender/tests/cert.txt") as file:
        return file.read()


class TesteCertificateA1:
    cer_base64 = get_cert_base64()
    password = "1234"

    certificate = CertificateA1(cer_base64, password)

    def test_name(self):
        assert self.certificate.owner == "Wayne Enterprises, Inc"

    def test_CNPJ(self):
        assert self.certificate.CNPJ == None


class TestSefazRequest:
    def test_status_servico(self):
        url, service, etree_xml = SefazRequest().status_servico()

        assert (
            url
            == "https://hom.sefazvirtual.fazenda.gov.br/NFeStatusServico4/NFeStatusServico4.asmx?wsdl"
        )

        assert service == "nfeStatusServicoNF"

        assert (
            etree.tostring(etree_xml).decode()
            == '<consStatServ xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00"><tpAmb>2</tpAmb><cUF>21</cUF><xServ>STATUS</xServ></consStatServ>'
        )

    def test_consulta_protocolo(self):
        url, service, etree_xml = SefazRequest().consulta_protocolo(
            "21210603867404000175550010000013091000436891"
        )

        assert (
            url
            == "https://hom.sefazvirtual.fazenda.gov.br/NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx?wsdl"
        )

        assert service == "nfeConsultaNF"

        assert (
            etree.tostring(etree_xml).decode()
            == '<consSitNFe xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00"><tpAmb>2</tpAmb><xServ>CONSULTAR</xServ><chNFe>21210603867404000175550010000013091000436891</chNFe></consSitNFe>'
        )

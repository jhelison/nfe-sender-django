from cryptography.x509.base import Certificate
from packages.core.certificate import CertificateA1


def get_cert_base64():
    with open("./nfe_sender/tests/cert.txt") as file:
        return file.read()


class TesteCertificateA1:
    cer_base64 = get_cert_base64()
    password = "1234"

    certificate = CertificateA1(cer_base64, password)

    print(str(certificate.not_valid_before))

    def test_name(self):
        assert self.certificate.owner == "Wayne Enterprises, Inc"

    def test_CNPJ(self):
        assert self.certificate.CNPJ == None

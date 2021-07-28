from datetime import datetime
from typing import List, Tuple
import base64
from OpenSSL import crypto
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12
import tempfile
import os


class CertificateA1:
    def __init__(self, b64_certificate: str, password: str) -> None:
        self._certificate_file = CertificateA1.binary_from_base64(b64_certificate)
        self._password = password.encode()
            
        try:
            self._pkcs12 = crypto.load_pkcs12(self._certificate_file, self._password)
        except crypto.Error:
            raise Exception("Certificado ou senha invalida")
            

        self._certificate = crypto.dump_certificate(
            crypto.FILETYPE_PEM, self._pkcs12.get_certificate()
        )
        
        self._private_key = crypto.dump_privatekey(
            crypto.FILETYPE_PEM, self._pkcs12.get_privatekey()
        )

        self._x509 = crypto.load_certificate(crypto.FILETYPE_PEM, self._certificate)

        self.key, self.cert, _ = pkcs12.load_key_and_certificates(
            data=self._certificate_file,
            password=self._password,
            backend=default_backend(),
        )

    def cert_key(self) -> Tuple[str, str]:
        return self._certificate.decode(), self._private_key.decode()
    
    @staticmethod
    def binary_from_base64(b64_string: str) -> bytes:
        return base64.b64decode(b64_string)
    
    @property
    def not_valid_before(self):
        return self.cert.not_valid_before
    
    @property
    def not_valid_after(self):
        return self.cert.not_valid_after
    
    @property
    def issuer(self):
        return self._x509.get_subject().OU
    
    @property
    def expired(self):
        return self._x509.has_expired()
    
    @property
    def CNPJ(self):
        subject = self._x509.get_subject().CN
        if ':' in subject:
            return subject.split(':')[1]
        
    @property
    def owner(self):
        subject = self._x509.get_subject().CN
        if ':' in subject:
            return subject.split(':')[0]


class CertificateAsFile:
    def __init__(self, certificate: CertificateA1) -> None:
        self.key_fd, self.key_path = tempfile.mkstemp()
        self.cert_fd, self.cert_path = tempfile.mkstemp()

        cert, key = certificate.cert_key()

        tmp = os.fdopen(self.key_fd, "w")
        tmp.write(cert)
        # print(cert)

        tmp = os.fdopen(self.cert_fd, "w")
        tmp.write(key)
        # print(key)

    def __enter__(self):
        return self.key_path, self.cert_path

    def __exit__(self, type, value, traceback):
        os.remove(self.key_path)
        os.remove(self.cert_path)


# cert_path = r"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"
# password = "81979780"
# cert = CertificateA1(cert_path, password)
# print(cert.not_valid_before)
# print(cert.not_valid_after)
# print(cert.issuer)
# print(cert.expired)
# print(cert.CNPJ)
# print(cert.owner)
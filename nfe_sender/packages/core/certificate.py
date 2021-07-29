from typing import List, Tuple
import base64
from OpenSSL import crypto
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12
import tempfile
import os


class CertificateA1:
    """
    Generate a class loaded with a base64 encoded pfx pkcs12 certificate.
    """

    def __init__(self, b64_certificate: str, password: str) -> None:
        self._certificate_file = CertificateA1.binary_from_base64(b64_certificate)
        self._password = password.encode()

        self._pkcs12 = crypto.load_pkcs12(self._certificate_file, self._password)

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
        """
        Returns the certificate and private key
        """
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
        if ":" in subject:
            return subject.split(":")[1]

    @property
    def owner(self):
        subject = self._x509.get_subject().CN
        if ":" in subject:
            return subject.split(":")[0]
        else:
            return subject


class CertificateAsFile:
    """
    Uses the certificate and private as temporary files
    """

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

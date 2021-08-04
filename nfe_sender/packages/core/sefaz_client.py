from contextlib import contextmanager
import os
import tempfile
from packages.core.certificate import CertificateA1, CertificateAsFile
import requests
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.cache import SqliteCache
from lxml import etree

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)


class SefazClient:
    """
    It generates the client connected to Sefaz server.

    Having a certificate ready with can be used as:
    with SefazClient.get_client(cert, url) as client:
        client ...
    """

    def __init__(self, cert: CertificateA1) -> None:
        self.cert = cert

    @contextmanager
    def get_client(self, url: str) -> Client:
        with CertificateAsFile(self.cert) as (key, cert):
            session = Session()
            session.cert = (key, cert)
            session.verify = False

            transport = Transport(session=session, cache=self._get_cache())

            self._client = Client(url, transport=transport)

            try:
                yield self._client
            finally:
                self._client = False

    @staticmethod
    def _get_cache():
        temp_dir = tempfile.gettempdir()
        cache_file = os.path.join(temp_dir, "transmition.db")
        return SqliteCache(path=cache_file, timeout=60)

    def post(self, url: str, service: str, etree_data: etree.Element) -> etree.Element:
        with self.get_client(url) as client:
            res = client.service[service](etree_data)
            return res

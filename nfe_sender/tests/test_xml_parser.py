from packages.core.xml_parser import NFeParser

nfe_str = open(r"nfe_sender\tests\nfe_signed.xml", "r").read()
dev_str = open(r"nfe_sender\tests\dev.xml", "r").read()

class TestNFeParser:

    nfe = NFeParser(nfe_str)

    def test_is_valid(self):
        assert self.nfe.is_valid

    def test_remove_signature(self):
        self.nfe.remove_signature()
        for child in self.nfe.root.iter("*"):
            assert not child.tag.endswith("Signature")

    def test_uri(self):
        assert self.nfe.uri == "NFe21210703867404000175550010000013441000431051"


# class TestCancelamentoParser:

#     canc = CancelamentoParser(dev_str)

#     def test_is_valid(self):
#         assert self.canc.is_valid

#     def test_remove_signature(self):
#         self.canc.remove_signature()
#         for child in self.canc.root.iter("*"):
#             assert not child.tag.endswith("Signature")

#     def test_uri(self):
#         assert self.canc.uri == "ID21210703867404000175550010000014221000461897"

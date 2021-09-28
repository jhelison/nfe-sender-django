from __future__ import annotations
from copy import deepcopy
from typing import Union
from lxml import etree
from .signer import Signer, CertificateA1
import xmltodict
from json import loads, dumps
import re
from datetime import datetime

NSMAP = {None: "http://www.portalfiscal.inf.br/nfe"}
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
        new_root = deepcopy(self.root)

        for child in new_root.iter("*"):
            if etree.QName(child).localname == "tpAmb":
                child.text = "2"
                break

        for child in new_root.iter("*"):
            if etree.QName(child).localname == "dest":
                for grandchild in child.iter("*"):
                    if etree.QName(grandchild).localname == "xNome":
                        grandchild.text = (
                            "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"
                        )
                        break

        self.root = new_root

    def sign(self, certificate: CertificateA1) -> None:
        self.remove_signature()

        self.root = Signer(certificate).sign_xml(xml=self.root, uri=self.uri)

    def find_text_from_tag(self, tag: str):
        for child in self.root.iter("*"):
            if etree.QName(child).localname == tag:
                return child.text
        return None

    def child_XMLParser(self, tag: str):
        """
        Return a XMLParser with the found child tag.
        """
        for child in self.root.iter("*"):
            if etree.QName(child).localname == tag:
                return XMLParser(child)
        return None

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
    
    def remove_namespaces(self):
        new_root = deepcopy(self.root)
        for child in new_root.getiterator():
            child.tag = etree.QName(child).localname
        etree.cleanup_namespaces(new_root)
        
        self.root = new_root
        
    def clean_root(self, nsmap: bool = True):
        nsmap = NSMAP if nsmap else None
                
        root_tag = etree.QName(self.root).localname
        new_root = etree.Element(root_tag, nsmap=nsmap, **self.root.attrib)
        
        for child in self.root:
            new_root.append(child)
                        
        self.root = new_root


    @staticmethod
    def _remove_metatag(xml: str) -> str:
        return re.sub(r"<\?xml([\s\S]*?)\?>", "", xml)

    def __repr__(self) -> str:
        return etree.tostring(self.root, encoding="UTF-8").decode()


class NFeParser(XMLParser):
    def __init__(self, xml: str) -> None:
        super().__init__(xml)
        self._clean_nfe_tree()

    def _clean_nfe_tree(self) -> None:
        xml_tree = deepcopy(self.root)
        NFe_root = etree.Element("NFe", nsmap=NSMAP)

        for child in xml_tree:
            NFe_root.append(child)

        for child in NFe_root.iter("*"):
            if child.text is not None and not child.text.strip():
                child.text = None

        self.root = NFe_root

    def is_valid(self) -> bool:
        return etree.QName(self.root).localname == "NFe"


class EventoParser(XMLParser):
    def __init__(self, xml: str) -> None:
        super().__init__(xml)
        
    @staticmethod
    def cancelamento_is_valid(xml: str):
        canc = XMLParser(xml)
        
        n_prot = canc.find_text_from_tag("nProt")
        x_just = canc.find_text_from_tag("xJust")
        ch_nfe = canc.find_text_from_tag("chNFe")
        
        return n_prot and x_just and ch_nfe
    
    @staticmethod
    def carta_is_valid(xml: str):
        carta = XMLParser(xml)

        ch_nfe = carta.find_text_from_tag("ChaveAcesso")
        x_correcao = carta.find_text_from_tag("Correcao")
        
        return ch_nfe and x_correcao

    @classmethod
    def evento_from_cancelamento(
        cls, xml: str, cnpj: str, uf: str = 21, is_hom: bool = True
    ) -> XMLParser:
        canc = XMLParser(xml)

        n_prot = canc.find_text_from_tag("nProt")
        x_just = canc.find_text_from_tag("xJust")
        ch_nfe = canc.find_text_from_tag("chNFe")

        det_evento = etree.Element("detEvento", versao="1.00")
        det_evento.append(el_with_text("descEvento", "Cancelamento"))
        det_evento.append(el_with_text("nProt", n_prot))
        det_evento.append(el_with_text("xJust", x_just))

        evento = cls.build_evento(
            chNFe=ch_nfe,
            cnpj=cnpj,
            uf=uf,
            is_hom=is_hom,
            det_evento=det_evento,
            tp_evento="110111",
        )

        return XMLParser(evento)

    @classmethod
    def evento_from_carta(
        cls, xml: str, cnpj: str, uf: str = 21, is_hom: bool = True
    ) -> XMLParser:
        carta = XMLParser(xml)

        ch_nfe = carta.find_text_from_tag("ChaveAcesso")
        x_correcao = carta.find_text_from_tag("Correcao")

        det_evento = etree.Element("detEvento", versao="1.00")
        det_evento.append(el_with_text("descEvento", "Carta de Correcao"))
        det_evento.append(el_with_text("xCorrecao", x_correcao))
        det_evento.append(
            el_with_text(
                "xCondUso",
                "A Carta de Correcao e disciplinada pelo paragrafo 1o-A do art. 7o do Convenio S/N, de 15 de dezembro de 1970 e pode ser utilizada para regularizacao de erro ocorrido na emissao de documento fiscal, desde que o erro nao esteja relacionado com: I - as variaveis que determinam o valor do imposto tais como: base de calculo, aliquota, diferenca de preco, quantidade, valor da operacao ou da prestacao; II - a correcao de dados cadastrais que implique mudanca do remetente ou do destinatario; III - a data de emissao ou de saida.",
            )
        )

        evento = cls.build_evento(
            chNFe=ch_nfe,
            cnpj=cnpj,
            uf=uf,
            is_hom=is_hom,
            det_evento=det_evento,
            tp_evento="110110",
        )

        return XMLParser(evento)

    @staticmethod
    def build_evento(
        chNFe: str,
        cnpj: str,
        det_evento: etree.Element,
        tp_evento: str,
        uf: int = 21,
        is_hom: bool = True,
    ):
        tp_amb = 2 if is_hom else 1
        dh_evento = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S-03:00")
        n_seq_evento = "01"

        id = "ID" + tp_evento + chNFe + n_seq_evento

        evento = etree.Element("evento", nsmap=NSMAP, versao="1.00")
        inf_evento = etree.Element("infEvento", Id=id)
        inf_evento.append(el_with_text("cOrgao", uf))
        inf_evento.append(el_with_text("tpAmb", tp_amb))
        inf_evento.append(el_with_text("CNPJ", cnpj))
        inf_evento.append(el_with_text("chNFe", chNFe))
        inf_evento.append(el_with_text("dhEvento", dh_evento))
        inf_evento.append(el_with_text("tpEvento", tp_evento))
        inf_evento.append(el_with_text("nSeqEvento", "1"))
        inf_evento.append(el_with_text("verEvento", "1.00"))
        inf_evento.append(det_evento)
        evento.append(inf_evento)

        return evento


class ReponseParser:
    def __init__(self, response: etree.Element, xml_signed: XMLParser) -> None:
        self.response = XMLParser(response)
        self.xml_signed = xml_signed

    def lote_status(self):
        return self.response.find_text_from_tag("cStat")

    def x_motivo(self):
        return self.response.find_text_from_tag("xMotivo")
    
    def nfe_response(self):
        self.response.remove_namespaces()
        
        if self.lote_status():
            prot_nfe = self.response.child_XMLParser("protNFe")

            return {
                "lote_is_sucessfull": self.lote_status() == "104",
                "lote_status": self.lote_status(),
                "lote_motivo": self.x_motivo(),
                "nfe_is_sucessfull": prot_nfe.find_text_from_tag("cStat") == "100",
                "nfe_status": prot_nfe.find_text_from_tag("cStat"),
                "nfe_motivo": prot_nfe.find_text_from_tag("xMotivo"),
                **self.response.dict,
                "nfe-ret": str(self.response),
                "nfe-sign": str(self.xml_signed),
                "proc-nfe": self._get_proc_nfe(prot_nfe=prot_nfe),
            }
        else:            
            return {
                "lote_is_sucessfull": self.lote_status() == "104",
                "lote_status": self.lote_status(),
                **self.response.dict,
                "nfe-ret": str(self.response),
                "nfe-sign": str(self.xml_signed),
            }

    def _get_proc_nfe(self, prot_nfe: XMLParser):
        xml_signed = str(self.xml_signed)
        prot_nfe = str(prot_nfe.child_XMLParser("protNFe"))
        
        proc_nfe = f'<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">{xml_signed}{prot_nfe}</nfeProc>'
        return proc_nfe
    
    def evento_response(self):       
        if self.lote_status():
            ret_evento = self.response.child_XMLParser("retEvento")
            
            return {
                "lote_is_sucessfull": self.lote_status() == "128",
                "lote_status": self.lote_status(),
                "lote_motivo": self.x_motivo(),
                "evento_is_sucessfull": ret_evento.find_text_from_tag("cStat") == "135",
                "evento_status": ret_evento.find_text_from_tag("cStat"),
                "evento_motivo": ret_evento.find_text_from_tag("xMotivo"),
                **self.response.dict,
                "evento-ret": str(self.response),
                "can_get": self.get_can_get(),
                "evento": str(self.xml_signed)
            }
            
        else:
            return {
                "lote_is_sucessfull": self.lote_status() == "128",
                "lote_status": self.lote_status(),
                "lote_motivo": self.x_motivo(),
                **self.response.dict,
                "evento": str(self.xml_signed)
            }

    def get_can_get(self):
        self.response.clean_root()  
        response = str(self.response)
        nfe_resul_msg = f'<nfeResultMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeRecepcaoEvento4">{response}</nfeResultMsg>'
        
        return nfe_resul_msg

def el_with_text(tag: str, text: any) -> etree.Element:
    """
    Returns a etree element with a set tag and text inside
    """
    el = etree.Element(tag)
    el.text = str(text)

    return el

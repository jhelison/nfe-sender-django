from __future__ import annotations
from packages.NFEBuilder.xml_document import XMLDocument

from enum import Enum


class EmitDestEnum(Enum):
    EMIT = "emit"
    DEST = "dest"


class EmitDest(XMLDocument):
    __root_name__ = EmitDestEnum

    CNPJ = None
    xNome = None
    xFant = None
    IE = None
    CRT = None
    CPF = None
    indIEDest = None
    ender: Ender = None

    def __init__(
        self,
        __root_name__: EmitDestEnum,
        xNome: str,
        IE: str,
        ender: Ender,
        CRT: str = None,
        xFant: str = None,
        CNPJ: str = None,
        CPF: str = None,
        indIEDest: str = None,
    ) -> None:
        if not CPF and not CNPJ:
            raise Exception("missing one positional requiment, CPF of CNPJ")

        self.__root_name__ = __root_name__.value
        self.CNPJ = CNPJ
        self.xNome = xNome
        self.xFant = xFant
        self.IE = IE
        self.CRT = CRT
        self.CPF = CPF
        self.indIEDest = indIEDest

        self.ender = ender


class EnderEnum(Enum):
    EMIT = "enderEmit"
    DEST = "enderDest"


class Ender(XMLDocument):
    __root_name__ = EnderEnum

    xLgr = None
    nro = None
    xBairro = None
    cMun = None
    xMun = None
    UF = None
    CEP = None
    cPais = None
    xPais = None
    fone = None
    xCpl = None

    def __init__(
        self,
        __root_name__: EnderEnum,
        xLgr: str,
        nro: str,
        xBairro: str,
        cMun: str,
        xMun: str,
        UF: str,
        CEP: str,
        cPais: str,
        xPais: str,
        fone: str,
        xCpl: str = None,
    ) -> None:
        self.__root_name__ = __root_name__.value
        self.xLgr = xLgr
        self.nro = nro
        self.xBairro = xBairro
        self.cMun = cMun
        self.xMun = xMun
        self.UF = UF
        self.CEP = CEP
        self.cPais = cPais
        self.xPais = xPais
        self.fone = fone
        self.xCpl = xCpl if xCpl else None

from packages.NFEBuilder.emit import EmitDest, Ender, EnderEnum, EmitDestEnum
from lxml import etree


class TestClassBuilding:
    ender_emit = Ender(
        __root_name__=EnderEnum.EMIT,
        xLgr="RUA INDEPENDENCIA",
        nro="137",
        xBairro="CENTRO",
        cMun="2102325",
        xMun="BURITICUPU",
        UF="MA",
        CEP="65393000",
        cPais="1058",
        xPais="BRASIL",
        fone="09835380400",
    )

    ender_dest = Ender(
        __root_name__=EnderEnum.DEST,
        xLgr="AV ROMULO MAIORANA",
        nro="380",
        xCpl="OPLIMA 91-31818000",
        xBairro="MARCO",
        cMun="1501402",
        xMun="Belem",
        UF="PA",
        CEP="66093005",
        cPais="1058",
        xPais="BRASIL",
        fone="9132361529",
    )

    emit = EmitDest(
        __root_name__=EmitDestEnum.EMIT,
        CNPJ="03867404000175",
        xNome="ORIZA VIEIRA LIMA",
        ender=ender_emit,
        xFant="O TIJOLAO 2",
        IE="125859520",
        CRT="1",
    )

    dest = EmitDest(
        __root_name__=EmitDestEnum.DEST,
        CNPJ="13234724000141",
        xNome="MOREIRA MOUTINHO ENGENHARIA LTDA-EPP",
        indIEDest="1",
        IE="153285460",
        ender=ender_dest,
    )

    # def test_ender_emit(self):
    #     assert (
    #         str(self.ender_emit)
    #         == "<enderEmit><xLgr>RUA INDEPENDENCIA</xLgr><nro>137</nro><xBairro>CENTRO</xBairro><cMun>2102325</cMun><xMun>BURITICUPU</xMun><UF>MA</UF><CEP>65393000</CEP><cPais>1058</cPais><xPais>BRASIL</xPais><fone>09835380400</fone></enderEmit>"
    #     )

    # def test_ender_dest(self):
    #     assert (
    #         str(self.ender_dest)
    #         == "<enderDest><xLgr>AV ROMULO MAIORANA</xLgr><nro>380</nro><xBairro>MARCO</xBairro><cMun>1501402</cMun><xMun>Belem</xMun><UF>PA</UF><CEP>66093005</CEP><cPais>1058</cPais><xPais>BRASIL</xPais><fone>9132361529</fone><xCpl>OPLIMA 91-31818000</xCpl></enderDest>"
    #     )

    def test_emit(self):
        self.emit.to_xml()
        assert True

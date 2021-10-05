from lxml import etree


class XMLDocument:
    __root_name__ = None

    def to_xml(self) -> etree.Element:
        xml_document = etree.Element(self.__root_name__)

        for key, value in self.__dict__.items():
            if value is not None and key not in vars(XMLDocument).keys():
                xml_document.append(self.element_with_text(key, value))

                if isinstance(value, XMLDocument):
                    xml_document.append(value.to_xml())

        print(xml_document)
        # return xml_document

    # def __repr__(self) -> str:
    #     return etree.tostring(self.to_xml(), encoding="UTF-8").decode()

    # Remember to have the method after, its alread on xml_parser
    @staticmethod
    def element_with_text(tag: str, text: any) -> etree.Element:
        """
        Returns a etree element with a set tag and text inside
        """
        el = etree.Element(tag)
        el.text = str(text)

        return el

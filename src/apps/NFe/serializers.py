from rest_framework import serializers
from packages.sender.xml_parser import NFeParser, EventoParser


class NFESerializer(serializers.Serializer):
    xml = serializers.CharField()

    def validate_xml(self, xml):
        try:
            nfe = NFeParser(xml)
            if not nfe.is_valid():
                raise serializers.ValidationError("Erro ao ler xml")
        except:
            raise serializers.ValidationError("Erro ao ler xml")

        return xml


class CancelamentoSerializer(serializers.Serializer):
    xml = serializers.CharField()

    def validate_xml(self, xml):
        try:
            if not EventoParser.cancelamento_is_valid(xml):
                raise serializers.ValidationError("Erro ao ler xml")
        except:
            raise serializers.ValidationError("Erro ao ler xml")

        return xml


class CartaSerializer(serializers.Serializer):
    xml = serializers.CharField()

    def validate_xml(self, xml):
        try:
            if not EventoParser.carta_is_valid(xml):
                raise serializers.ValidationError("Erro ao ler xml")
        except:
            raise serializers.ValidationError("Erro ao ler xml")

        return xml

from rest_framework import serializers
from packages.core.xml_parser import NFeParser, CancelamentoParser


def validate_NFe(value):
    try:
        nfe = NFeParser(value)
    except:
        serializers.ValidationError("Erro ao ler xml")

    if not nfe.is_valid:
        serializers.ValidationError("NFe invalida")


class XMLSerializer(serializers.Serializer):
    xml = serializers.CharField(validators=[validate_NFe])


def validade_cancelamento(value):
    try:
        canc = CancelamentoParser(value)
    except:
        serializers.ValidationError("Erro ao ler xml")

    if not canc.is_valid:
        serializers.ValidationError("Cancelamento invalido")

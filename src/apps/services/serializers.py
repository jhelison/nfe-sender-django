from rest_framework import serializers


class ConsultaProtocoloSerializer(serializers.Serializer):
    chNFe = serializers.CharField(max_length=44)

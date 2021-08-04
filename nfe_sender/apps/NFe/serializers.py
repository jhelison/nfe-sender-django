from rest_framework import serializers
from lxml import etree

class AutorizacaoSerializer(serializers.Serializer):
    NFe = serializers.CharField()
    
    def validate(self, data):
        try:
            etree.fromstring(data["NFe"])
            return data
        except:
            raise serializers.ValidationError("NFe invalida")
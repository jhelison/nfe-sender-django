from rest_framework import serializers
from lxml import etree

class XMLSerializer(serializers.Serializer):
    xml = serializers.CharField()
    
    def validate(self, data):
        try:
            etree.fromstring(data["xml"])
            return data
        except:
            raise serializers.ValidationError("xml invalido")
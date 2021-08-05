from rest_framework import serializers
from lxml import etree


class XMLSerializer(serializers.Serializer):
    xml = serializers.CharField()

    def validate(self, data):
        try:
            print(data["xml"])
            etree.fromstring(data["xml"])
            return data
        except Exception as e:
            print(e)
            raise serializers.ValidationError("xml invalido")

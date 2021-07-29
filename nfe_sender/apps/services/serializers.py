from rest_framework import serializers

from packages.core.certificate import CertificateA1


class StatusSerializer(serializers.Serializer):
    hom = serializers.BooleanField()
    certificate = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate the certificate
        """
        try:
            CertificateA1(data["certificate"], data["password"])
            return data
        except:
            raise serializers.ValidationError("Certificado ou senha invalidos")

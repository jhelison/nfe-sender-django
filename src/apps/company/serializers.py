from rest_framework import serializers
from packages.core.certificate import CertificateA1
from rest_framework.authtoken.models import Token
import re

from apps.company.models import CustomUser


def validate_cnpj(cnpj):
    """
    Valida CNPJs, retornando apenas a string de números válida.
    """
    cnpj = "".join(re.findall("\d", str(cnpj)))

    if (not cnpj) or (len(cnpj) < 14):
        raise serializers.ValidationError("CNPJ invalido")

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return

    raise serializers.ValidationError("CNPJ invalido")


def username_is_unique(username):
    try:
        CustomUser.objects.get(username=username)
    except:
        return

    raise serializers.ValidationError("Empresa já cadastrada")


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=14, validators=[validate_cnpj, username_is_unique]
    )
    company_name = serializers.CharField(max_length=80)
    uf = serializers.IntegerField(required=False)
    is_hom = serializers.BooleanField(required=False)
    base64_certificate = serializers.CharField()
    certificate_password = serializers.CharField(max_length=80)

    def validate(self, data):
        """
        Validate the certificate
        """
        try:
            CertificateA1(data["base64_certificate"], data["certificate_password"])
            return data
        except:
            raise serializers.ValidationError("Certificado ou senha invalidos")

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)


class RecoverSerializer(serializers.Serializer):
    base64_certificate = serializers.CharField()
    certificate_password = serializers.CharField(max_length=80)

    def validate(self, data):
        """
        Validate the certificate
        """
        try:
            CertificateA1(data["base64_certificate"], data["certificate_password"])
        except:
            raise serializers.ValidationError("Certificado ou senha invalidos")

        try:
            self.user = CustomUser.objects.get(
                certificate_password=data["certificate_password"],
                base64_certificate=data["base64_certificate"],
            )
        except:
            raise serializers.ValidationError("Usuário não encontrado")

        return data

    def get_token(self):
        token, _ = Token.objects.get_or_create(user=self.user)

        return token.key

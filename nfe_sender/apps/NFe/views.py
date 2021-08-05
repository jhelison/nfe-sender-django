from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import XMLSerializer
from packages.core.process_request import process_autorizacao, process_cancelamento


class AutorizacaoView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = XMLSerializer(data=request.data)

        if serializer.is_valid():
            response = process_autorizacao(
                base64_certificate=request.user.base64_certificate,
                certificate_password=request.user.certificate_password,
                is_hom=request.user.is_hom,
                xml=serializer.data["xml"],
            )

            return Response(response)

        return Response(serializer.errors)


class CancelamentoView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = XMLSerializer(data=request.data)

        if serializer.is_valid():
            response = process_cancelamento(
                base64_certificate=request.user.base64_certificate,
                certificate_password=request.user.certificate_password,
                is_hom=request.user.is_hom,
                xml=serializer.data["xml"],
            )

            return Response(response)

        return Response(serializer.errors)


@api_view(["GET"])
def root_view(request):
    return Response(
        {
            "autorizacao": reverse("autorizacao", request=request),
            "cancelamento": reverse("cancelamento", request=request),
        }
    )

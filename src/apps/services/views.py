from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import ConsultaProtocoloSerializer
from packages.core.process_request import process_status, process_consulta_protocolo

# , process_consulta_protocolo


class StatusServicoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = process_status(user_data=vars(request.user))

        return Response(response)


class ConsultaProtocoloView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ConsultaProtocoloSerializer(data=request.data)

        if serializer.is_valid():
            response = process_consulta_protocolo(
                user_data=vars(request.user),
                chNFe=serializer.data["chNFe"],
            )

            return Response(response)

        return Response(serializer.errors)


@api_view(["GET"])
def root_view(request):
    return Response(
        {
            "status": reverse("services-status", request=request),
            "consulta protocolo": reverse("consulta-protocolo", request=request),
        }
    )

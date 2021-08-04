from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import AutorizacaoSerializer
from packages.core.process_request import process_autorizacao

class AutorizacaoView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = AutorizacaoSerializer(data=request.data)
        
        if serializer.is_valid():
            response = process_autorizacao(
                base64_certificate=request.user.base64_certificate,
                certificate_password=request.user.certificate_password,
                is_hom=request.user.is_hom,
                NFe=serializer.data["NFe"],
            )
            
            return Response(response)
        
        return Response(serializer.errors)

@api_view(["GET"])
def root_view(request):
    return Response(
        {
            "autorizacao": reverse("autorizacao", request=request)
        }
    )
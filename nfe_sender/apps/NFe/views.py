from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import AutorizacaoSerializer

class AutorizacaoView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = AutorizacaoSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response("wow")
        
        return Response(serializer.errors)

@api_view(["GET"])
def root_view(request):
    return Response(
        {
            "autorizacao": reverse("autorizacao", request=request)
        }
    )
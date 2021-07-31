from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import StatusSerializer
from packages.core.request_builder import process_status


class NfeStatusServico(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        server_status = process_status(request.user.base64_certificate, request.user.certificate_password)
        
        return Response(server_status)


@api_view(["GET"])
def root(request):
    return Response({"status": reverse("services-status", request=request)})

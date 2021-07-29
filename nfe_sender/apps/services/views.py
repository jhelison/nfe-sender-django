from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import StatusSerializer
from packages.core import request_builder


@api_view(["POST"])
def nfe_status_servico(request):
    serializer = StatusSerializer(data=request.data)

    if serializer.is_valid():
        status = request_builder.process_status(serializer.validated_data)
        return Response(status)

    return Response(serializer.errors)


@api_view(["GET"])
def root(request):
    return Response({"status": reverse("services-status", request=request)})

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def server_status(request):
    return Response({
        "status":"Working",
    })
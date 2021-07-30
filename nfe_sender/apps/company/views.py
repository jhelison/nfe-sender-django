from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import UserAuthSerializer

@api_view(["POST"])
def sign_in(request):
    serializer = UserAuthSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.validated_data)
    
    return Response(serializer.errors)
    
@api_view(["GET"])
def root(request):
    return Response({"sign-in": reverse("sign-in", request=request)})
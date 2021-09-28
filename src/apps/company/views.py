from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from .serializers import UserAuthSerializer, RecoverSerializer


@api_view(["POST"])
def sign_in(request):
    serializer = UserAuthSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        token = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

    return Response(serializer.errors)


@api_view(["POST"])
def recover_token(request):
    serializer = RecoverSerializer(data=request.data)

    if serializer.is_valid():
        return Response({"token": serializer.get_token()})
    return Response(serializer.errors)


@api_view(["GET"])
def root(request):
    return Response(
        {
            "sign-in": reverse("sign-in", request=request),
            "recover": reverse("recover", request=request),
        }
    )

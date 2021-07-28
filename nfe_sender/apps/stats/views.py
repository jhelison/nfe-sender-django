from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

import subprocess

@api_view(['GET'])
def server_status(request):
    return Response({
        "status":"Working",
        "version": subprocess.run(['poetry', 'version', '-s'], capture_output=True, text=True).stdout.rstrip()
    })
    
@api_view(['GET'])
def stats_root(request):
    return Response({
        'status': reverse('stats-status', request=request)
    })
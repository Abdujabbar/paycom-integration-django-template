from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .paycom import Paycom
from .exceptions import PaycomException
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# Create your views here.
@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def index(request):
    paycom = Paycom(request)
    try:
        paycom.authorize()
    except PaycomException as e:
        return Response({
            "id": paycom.params['id'],
            "result": "",
            "error": e.ERRORS["UNAUTHENTICATED"]
        })




    return Response({
        "success": True,
    })

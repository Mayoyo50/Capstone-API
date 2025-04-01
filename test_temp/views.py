from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getUser(request):
    person = {'name': 'Kevin', 'age': 33}
    return Response(person)

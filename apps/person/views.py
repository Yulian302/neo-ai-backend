from django.http import JsonResponse
from django.core import serializers
from rest_framework.views import APIView
import json
from .models import Person


# Create your views here.


class PersonList(APIView):
    def get(self, request):
        people = list(Person.objects.all().values())
        return JsonResponse(people, safe=False)

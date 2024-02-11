import json

from django.http import JsonResponse


def index(request):
    return JsonResponse(json.dumps({"Hello": "good"}), safe=False)

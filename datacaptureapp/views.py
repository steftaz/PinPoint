import json
from django.http import HttpResponse
from django.shortcuts import render


def geolocation(request):
    if request.method == 'POST':
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        response_data = {}
        response_data['message'] = latitude

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, "datacaptureapp/TestHtmlGeo.html")

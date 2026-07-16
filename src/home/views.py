from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

def home(request):
    return JsonResponse({ 
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"] }
    )
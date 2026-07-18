from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

tasks = [
    {"id": 1, "title": "Task 1", "done": True},
    {"id": 2, "title": "Task 2", "done": True},
    {"id": 3, "title": "Task 3", "done": False},
] # type: ignore

def get_tasks(request):
    return JsonResponse(tasks, safe=False)


def get_task(request, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return JsonResponse(task)

    return JsonResponse(
        {"error": "Task not found"},
        status=404
    )

def health(request):
    return JsonResponse({"status": "ok"})

def home(request):
    return JsonResponse({ 
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"] }
    )
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse

tasks = [
    {"id": 1, "title": "Read book", "done": False},
    {"id": 2, "title": "Exercise", "done": True},
] # type: ignore

@csrf_exempt
def tasks_view_create(request):
    if(request.method == "POST"):
        body = json.loads(request.body)
        # give "" if no title present as default view and trims whitespace at end & begining
        title = body.get("title","").strip()

        if not title:
            return JsonResponse(
                {"error" : "title is required"},
                status=400
            )
        
        next_id = max((task["id"] for task in tasks), default=0) + 1
        new_task = {
            "id": next_id,
            "title": title,
            "done": False
        }
        tasks.append(new_task)
        return JsonResponse(new_task, status=201)

    return JsonResponse(tasks, safe=False)

@csrf_exempt
def task_detail(request, task_id):
    task = next(
        (task for task in tasks if task["id"] == task_id),
        None
    )

    if not task:
        return JsonResponse(
            {"error": "Task not found"},
            status=404
        )

    if(request.method == "GET"):
        return JsonResponse(task)
    
    elif(request.method == "DELETE"):
        tasks.remove(task)
        return JsonResponse(
            {},
            status=204
        )

    elif(request.method == "PUT"):
        body = json.loads(request.body)
        if not body:
            return JsonResponse(
                {"error": "Request body cannot be empty"},
                status=400
            )
        
        title = body.get("title","").strip()
        if title:
            task["title"] = title

        if "done" in body:
            task["done"] = body["done"]

        return JsonResponse(task)
    


def health(request):
    return JsonResponse({"status": "ok"})

def home(request):
    return JsonResponse({ 
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"] }
    )
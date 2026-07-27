import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers


tasks = [
    {"id": 1, "title": "Read book", "done": False},
    {"id": 2, "title": "Exercise", "done": True},
]


# inline serializer as it was required for doc only
class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    done = serializers.BooleanField()

# create task, get all tasks apis
@extend_schema(
    methods=["GET"],
    responses=TaskSerializer(many=True),
    description="List all tasks",
)
@extend_schema(
    methods=["POST"],
    request=inline_serializer(name="TaskCreate", fields={"title": serializers.CharField()}),
    responses={
        201: TaskSerializer,
        400: OpenApiResponse(description="title is required"),
    },
    description="Create a new task",
)
@api_view(["GET", "POST"])
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

    # for get method
    return JsonResponse(tasks, safe=False)


# update, delete and get taks by id api
@extend_schema(
    methods=["GET"],
    responses={
        200: TaskSerializer,
        404: OpenApiResponse(description="Task not found")
    },
    description="Create a task by id",
)
@extend_schema(
    methods=["PUT"],
    request=inline_serializer(
        name="TaskUpdate",
        fields={
            "title": serializers.CharField(required=False),
            "done": serializers.BooleanField(required=False),
        },
    ),
    responses={
        200: TaskSerializer, 
        400: OpenApiResponse(description="empty body"),
        404: OpenApiResponse(description="Task not found")
    },
    description="update a task by id",
)
@extend_schema(
    methods=["DELETE"],
    responses={
        204: None, 
        404: OpenApiResponse(description="Task not found")
    },
    description="delete a task by id",
)
@api_view(["GET", "PUT", "DELETE"])
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

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON in request body"},
                status=400
            )
        
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
    

@extend_schema(
    description="Health check endpoint",
    responses={200: None},
)
@api_view(["GET"])
def health(request):
    return JsonResponse({"status": "ok"})


@extend_schema(
    description="Returns basic information about the API",
    responses={200: None},
)
@api_view(["GET"])
def home(request):
    return JsonResponse({ 
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"] }
    )
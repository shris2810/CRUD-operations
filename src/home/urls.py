from django.urls import path
from .views import home,health,get_tasks,get_task

urlpatterns = [
    path("", home, name="home"),
    path("health/", health, name="health"),
    path("tasks/", get_tasks, name="get_tasks"),
    path("tasks/<int:task_id>/", get_task, name="get_task")
]
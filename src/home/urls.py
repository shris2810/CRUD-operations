from django.urls import path
from .views import home,health,task_detail,tasks_view_create

urlpatterns = [
    path("", home, name="home"),
    path("health/", health, name="health"),
    path("tasks/", tasks_view_create, name="get_tasks"),
    path("tasks/<int:task_id>/", task_detail, name="get_task"),
]
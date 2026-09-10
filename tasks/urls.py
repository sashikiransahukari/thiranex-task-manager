from django.urls import path
from . import views
from . import api_views


urlpatterns = [

    # Website URLs
    path(
        "",
        views.login_view,
        name="login"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "edit/<int:task_id>/",
        views.edit_task,
        name="edit_task"
    ),

    path(
        "delete/<int:task_id>/",
        views.delete_task,
        name="delete_task"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    # API URLs
    path(
        "api/tasks/",
        api_views.TaskListCreateAPI.as_view(),
        name="api_task_list"
    ),

    path(
        "api/tasks/<int:task_id>/",
        api_views.TaskDetailAPI.as_view(),
        name="api_task_detail"
    ),
]
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Task


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not email or not password:
            error = "All fields are required."

        elif password != confirm_password:
            error = "Passwords do not match."

        elif User.objects.filter(username=username).exists():
            error = "Username already exists."

        elif User.objects.filter(email=email).exists():
            error = "Email already exists."

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)

            return redirect("dashboard")

    return render(
        request,
        "tasks/register.html",
        {"error": error}
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return redirect("dashboard")

        error = "Invalid username or password."

    return render(
        request,
        "tasks/login.html",
        {"error": error}
    )


@login_required
def dashboard(request):

    tasks = request.user.tasks.all().order_by("-created_at")

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date")

        if title:

            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date or None
            )

        return redirect("dashboard")

    total_tasks = tasks.count()

    pending_tasks = tasks.filter(
        status="pending"
    ).count()

    in_progress_tasks = tasks.filter(
        status="in_progress"
    ).count()

    completed_tasks = tasks.filter(
        status="completed"
    ).count()

    return render(
        request,
        "tasks/dashboard.html",
        {
            "tasks": tasks,
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
        }
    )


@login_required
def edit_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":

        task.title = request.POST.get("title")

        task.description = request.POST.get(
            "description"
        )

        task.priority = request.POST.get(
            "priority"
        )

        task.status = request.POST.get(
            "status"
        )

        task.due_date = (
            request.POST.get("due_date")
            or None
        )

        task.save()

        return redirect("dashboard")

    return render(
        request,
        "tasks/edit_task.html",
        {"task": task}
    )


@login_required
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":
        task.delete()

    return redirect("dashboard")


def logout_view(request):

    logout(request)

    return redirect("login")
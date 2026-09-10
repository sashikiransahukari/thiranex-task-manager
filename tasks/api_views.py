from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = TaskSerializer(
            tasks,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = TaskSerializer(
            data=request.data
        )

        if serializer.is_valid():

            task = serializer.save(
                user=request.user
            )

            return Response(
                TaskSerializer(task).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TaskDetailAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get_task(self, request, task_id):

        try:
            return Task.objects.get(
                id=task_id,
                user=request.user
            )

        except Task.DoesNotExist:
            return None

    def get(self, request, task_id):

        task = self.get_task(
            request,
            task_id
        )

        if task is None:
            return Response(
                {"error": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(task)

        return Response(
            serializer.data
        )

    def put(self, request, task_id):

        task = self.get_task(
            request,
            task_id
        )

        if task is None:
            return Response(
                {"error": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(
            task,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, task_id):

        task = self.get_task(
            request,
            task_id
        )

        if task is None:
            return Response(
                {"error": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        task.delete()

        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
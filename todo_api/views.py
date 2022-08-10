from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Todo
from .serializers import TodoSerializer

# Create your views here.


class TodoListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # list all
    def get(self, request, *args, **kwargs):
        todos = Todo.objects.filter(user=request.user.pk)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create
    def post(self, request, *args, **kwargs):
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.pk
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        try:
            return Todo.objects.get(id=todo_id, user=user_id)
        except Todo.DoesNotExist:
            return None

    def get(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.pk)
        if not todo_instance:
            return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        sereializer = TodoSerializer(todo_instance)
        return Response(sereializer.data, status=status.HTTP_200_OK)

    # updata
    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.pk)
        if not todo_instance:
            return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'task':request.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.pk
        }

        serializer = TodoSerializer(instance=todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete
    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.pk)
        if not todo_instance:
            return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        todo_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
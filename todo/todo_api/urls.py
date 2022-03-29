from django.urls import path
from .views import *

urlpatterns = [
    path('todo', TodoListApiView.as_view()),
    path('todo/<int:todo_id>/', TodoDetailApiView.as_view())
]
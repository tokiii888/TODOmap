from django.shortcuts import render
from .models import Todo
from django.http import HttpResponse

# Create your views here.

def index(request):
  latest_todo_list = Todo.objects.order_by('-updated_at')[:5]
  context={
    'latest_todo_list' : latest_todo_list
  }
  return render(request, 'todo/index.html', context)
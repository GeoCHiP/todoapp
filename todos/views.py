from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Task
from .forms import TaskForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todos:index')
        else:
            form = AuthenticationForm(request.POST)
    else:
        form = AuthenticationForm()

    context = { 'form': form }
    return render(request, 'todos/login.html', context)


@login_required(login_url=reverse_lazy('todos:login'))
def logout_view(request):
    logout(request)
    return redirect('todos:login')


@login_required(login_url=reverse_lazy('todos:login'))
def index(request):
    task_list = Task.objects.order_by('is_completed', '-created_date')

    context = { 'task_list': task_list }
    return render(request, 'todos/index.html', context)


@login_required(login_url=reverse_lazy('todos:login'))
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todos:index')
    else:
        form = TaskForm()

    context = { 'form': form }
    return render(request, 'todos/task_create.html', context)


@login_required(login_url=reverse_lazy('todos:login'))
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todos:index')
    else:
        form = TaskForm(instance=task)

    context = { 'task_id': task_id, 'form': form }
    return render(request, 'todos/task_update.html', context)


@login_required(login_url=reverse_lazy('todos:login'))
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('todos:index')

    context = { 'task': task }
    return render(request, 'todos/task_delete.html', context)


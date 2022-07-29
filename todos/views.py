from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('todos:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('todos:index')
    else:
        form = AuthenticationForm()

    context = { 'form': form }
    return render(request, 'todos/login.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('todos:index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todos:index')
    else:
        form = UserCreationForm()

    context = { 'form': form }
    return render(request, 'todos/register.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('todos:login')


@login_required
def index(request):
    task_list = Task.objects.order_by('is_completed', '-created_date')
    task_list = task_list.filter(user=request.user)
    incomplete_count = task_list.filter(is_completed=False).count()

    search_string = request.GET.get('search_string', '')
    if search_string:
        task_list = task_list.filter(task_title__icontains=search_string)

    context = {
        'task_list': task_list,
        'incomplete_count': incomplete_count,
        'search_string': search_string
    }
    return render(request, 'todos/index.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        task = Task(user=request.user)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todos:index')
    else:
        form = TaskForm()

    context = { 'form': form }
    return render(request, 'todos/task_create.html', context)


@login_required
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


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('todos:index')

    context = { 'task': task }
    return render(request, 'todos/task_delete.html', context)


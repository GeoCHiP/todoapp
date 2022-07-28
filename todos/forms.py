from django import forms

from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['user', 'task_title', 'task_description', 'is_completed']


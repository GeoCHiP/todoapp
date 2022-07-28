from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=200)
    task_description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_date = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        return self.task_title


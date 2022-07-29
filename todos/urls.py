from django.urls import path

from . import views

app_name = 'todos'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('task_create/', views.task_create, name='task_create'),
    path('task_update/<int:task_id>/', views.task_update, name='task_update'),
    path('task_delete/<int:task_id>/', views.task_delete, name='task_delete'),
]


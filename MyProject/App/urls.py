from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.EmailLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', views.UserCreateView.as_view(), name='user_create'),
    path('task/create', views.TaskCreateView.as_view(), name='task_create'),
    path('task/list', views.TaskListView.as_view(), name='task_list'),
    path('task/<str:pk>/detail', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<str:pk>/delete', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<str:pk>/update', views.TaskUpdateView.as_view(), name='task_update'),
]
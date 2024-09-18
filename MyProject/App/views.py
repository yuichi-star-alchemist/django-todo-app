from django.contrib.auth import hashers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
import random
from django.http import Http404

from .forms import EmailLoginForm, TaskForm, UserForm
from .models import AppUsers, Tasks


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class EmailLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = EmailLoginForm


class UserCreateView(CreateView):
    template_name = 'user_create.html'
    # model = AppUsers
    form_class = UserForm
    success_url = reverse_lazy('app:index')
    
    def form_valid(self, form):
        # パスワードをハッシュ化
        form.instance.password = hashers.make_password(form.cleaned_data["password"])
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user_update.html'
    model = AppUsers
    form_class = UserForm
    success_url = reverse_lazy('app:index')


class TaskCreateView(LoginRequiredMixin, CreateView):
    template_name = 'task_create.html'
    model = Tasks
    form_class = TaskForm
    success_url = reverse_lazy('app:index')
    
    def form_valid(self, form):
        form.instance.user_id = AppUsers.objects.get(id=self.request.user.pk)
        return super().form_valid(form)

class TaskListView(LoginRequiredMixin, ListView):
    template_name = 'task_list.html'
    model = Tasks
    
    def get_queryset(self):
        # ログインユーザーのデータをend_timeでソート
        return self.model.objects.filter(user_id=self.request.user.pk).order_by('end_time')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'task_update.html'
    model = Tasks
    form_class = TaskForm
    success_url = reverse_lazy('app:task_list')
    
    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.pk)

class TaskDeleteView(DeleteView):
    model = Tasks
    success_url = reverse_lazy('app:task_list')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # ログイン中のユーザーのpkとタスクのユーザーpkが一致するかチェック
        if obj.user_id.__str__() != str(self.request.user.pk):
            raise Http404('あなたはこのタスクを削除することはできません！')
        return obj
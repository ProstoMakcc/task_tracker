from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import CreateTaskForm, TaskFilterForm
from django.urls import reverse_lazy
from .mixins import UserIsOwnerMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status", "")

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)

        return context

class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"


class TaskCreateView(CreateView, LoginRequiredMixin):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(UpdateView, LoginRequiredMixin, UserIsOwnerMixin):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy("task-list")


class TaskDeleteView(DeleteView, LoginRequiredMixin, UserIsOwnerMixin):
    model = Task
    success_url = reverse_lazy("task-list")
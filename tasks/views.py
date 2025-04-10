from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Task, Comment, Like
from .forms import CreateTaskForm, TaskFilterForm, CommentForm
from django.urls import reverse_lazy
from .mixins import UserIsOwnerMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms


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

    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm(self.request.GET)

        return context
    
    def post(self, request, pk):
        comment_form = CommentForm(request.POST, request.FILES)
        task = self.get_object()

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            
        return redirect("task-detail", pk=comment.task.pk)
            

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


class CommentUpdateView(UpdateView, LoginRequiredMixin, UserIsOwnerMixin):
    model = Comment
    fields = ["content"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget.attrs.update({'class': 'input-field'})
        
        return form

    def form_valid(self, form):
        comment = self.get_object()
        if comment.author == self.request.user:
            return super().form_valid(form)
        
        raise PermissionError('Недостатньо прав')
    
    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={'pk': self.object.task.id})


class CommentDeleteView(DeleteView, LoginRequiredMixin, UserIsOwnerMixin):
    model = Comment

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={'pk': self.object.task.id})
    

class CommentLike(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        like_qs = Like.objects.filter(comment=comment, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            Like.objects.create(comment=comment, user=request.user)
        return HttpResponseRedirect(comment.get_absolute_url())
    
from django.db import models
from django.urls import reverse
from django.conf import settings


class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To do"),
        ("in_progress", "В прогресі"),
        ("done", "Виконано"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Низький"),
        ("medium", "Середній"),
        ("high", "Високий"),
        ("critical", "Критичний"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True) # Можна оставляти пустим
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return f"{self.title} with priority {self.priority}"
    
    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to="comments/", blank=True, null=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"
    
    def get_absolute_url(self):
        return self.task.get_absolute_url()


class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user') 

from django.urls import path
from tasks import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.TaskListView.as_view(), name="task-list"),
    path('<int:pk>/', views.TaskDetailView.as_view(), name="task-detail"),
    path('task-create/', views.TaskCreateView.as_view(), name="task-create"),
    path('task-update/<int:pk>/', views.TaskUpdateView.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', views.TaskDeleteView.as_view(), name="task-delete"),
    path('comment-update/<int:pk>/', views.CommentUpdateView.as_view(), name="comment-update"),
    path('comment-delete/<int:pk>/', views.CommentDeleteView.as_view(), name="comment-delete"),
    path('comment-like/<int:pk>/', views.CommentLike.as_view(), name="comment-like"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



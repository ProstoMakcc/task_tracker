from django.db import models
from django.contrib.auth.models import AbstractUser


class ExtendedUser(AbstractUser):
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.png")
    about_user = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

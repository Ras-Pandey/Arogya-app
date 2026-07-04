from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    security_question = models.CharField(max_length=200, blank=True, null=True)
    security_answer = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username
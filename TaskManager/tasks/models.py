from django.db import models
from django.conf import settings
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    description= models.TextField()
    completed= models.BooleanField(default=False)

    def __str__(self):
        return self.title

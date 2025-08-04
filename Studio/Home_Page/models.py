from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class ProjectInfo(models.Model):
    user = models.ForeignKey(User, related_name="Projects", on_delete=models.CASCADE)
    project = models.CharField(max_length=50,null=True)
    incomstatement = models.CharField(max_length=100,null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.project
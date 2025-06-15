from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ProjectInfo(models.Model):
    user = models.ForeignKey(User, related_name="Projects", on_delete=models.CASCADE)
    project = models.CharField(max_length=50,null=True)
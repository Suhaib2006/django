from django.db import models
from Home_Page.models import ProjectInfo
# Create your models here.
class DataInfo(models.Model):
        project= models.ForeignKey(ProjectInfo, related_name="Entrys", on_delete=models.CASCADE)
        code=models.CharField(max_length=50)
        name=models.CharField(max_length=100)
        amount=models.FloatField(default=float)
        entry=models.CharField(max_length=10)
        active=models.BooleanField(default=False)
        ledgerbalance=models.FloatField(default=float)

class CodeInfo(models.Model):
        project= models.ForeignKey(ProjectInfo, related_name="Codes", on_delete=models.CASCADE)
        code=models.CharField(max_length=50)

class TrialInfo(models.Model):
        project= models.ForeignKey(ProjectInfo, related_name="Trials", on_delete=models.CASCADE)
        name=models.CharField(max_length=100)
        amount=models.FloatField()
        state=models.CharField(max_length=10)
        order=models.IntegerField()

class Questionpaper(models.Model):
        project= models.ForeignKey(ProjectInfo, related_name="media", on_delete=models.CASCADE)
        pdf= models.FileField(upload_to='Question/')
        uploaded= models.BooleanField(False)

        def delete(self):
                self.pdf.delete()
                super().delete()
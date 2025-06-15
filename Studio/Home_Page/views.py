from django.shortcuts import render
from django.contrib.auth.models import User
from .models import ProjectInfo 
# Create your views here.

def Home_Page(request):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        if request.POST:
            project=request.POST.get('projectname').strip()
            if project != "":
                ProjectInfo.objects.create(user=user,project=project)
        project = user.Projects.all()
        length = len(project)
        Data={
            "User":user,
            "Project":project,
            "Length":length,
        }
        return render(request,'Home.html',Data)
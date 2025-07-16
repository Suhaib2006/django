from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import ProjectInfo 
# Create your views here.

def Home_Page(request):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        msg = ""
        if request.POST:
            project=request.POST.get('projectname').strip().lower()
            creat_date=request.POST.get('Date')
            if project != "":
                try:
                    ProjectInfo.objects.get(user=user,project=project)
                    msg = f"This {project} project name has already been taken"
                except:
                    ProjectInfo.objects.create(user=user,project=project,date=creat_date)
        project = user.Projects.all()
        length = len(project)
        Data={
            "User":user,
            "Project":project,
            "Length":length,
            "msg":msg,
        }
        return render(request,'Home.html',Data)

    return render(request,'Login.html')

def ProjectDelete(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        Data=ProjectInfo.objects.get(user=user,project=Project)
        Data.delete()
        return redirect('Home')
    

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import ProjectInfo 
from datetime import date
# Create your views here.

def Home_Page(request):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        msg = ""
        Date=date.today().isoformat()
        if request.POST:
            project=request.POST.get('projectname').strip().lower()
            incomestatment=request.POST.get('Incomstatement').strip().lower()
            creat_date=request.POST.get('Date')
            if project != "" and incomestatment!="Trade Mode":
                try:
                    ProjectInfo.objects.get(user=user,project=project)
                    msg = f"This {project} project name has already been taken"
                except:
                    ProjectInfo.objects.create(user=user,project=project,date=creat_date,incomstatement=incomestatment)
        project = user.Projects.all()
        length = len(project)
        Data={
            "User":user,
            "Project":project,
            "Length":length,
            "msg":msg,
            "Date":Date
        }
        return render(request,'Home.html',Data)

def ProjectDelete(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        Data=ProjectInfo.objects.get(user=user,project=Project)
        Data.delete()
        return redirect('Home')
    

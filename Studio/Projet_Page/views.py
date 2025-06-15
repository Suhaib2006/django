from django.shortcuts import render
from Home_Page.models import ProjectInfo
from .models import DataInfo,CodeInfo,TrialInfo
from django.contrib.auth.models import User
# Create your views here.

def Project_Page(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)
        if request.POST:
            Code=request.POST.get("Code").strip().upper()
            CodeInfo.objects.create(project=project,code=Code)

            for i in range(1,5):
                if request.POST.get(f"Name{i}").strip():
                    Name=request.POST.get(f"Name{i}").strip().lower()
                    Amount=request.POST.get(f"Amount{i}")
                    Entry="DR"
                    DataInfo.objects.create(project=project,code=Code,name=Name,amount=Amount,entry=Entry)
            for i in range(5,9):
                if request.POST.get(f"Name{i}").strip():
                    Name=request.POST.get(f"Name{i}").strip().lower()
                    Amount=request.POST.get(f"Amount{i}")
                    Entry="CR"
                    DataInfo.objects.create(project=project,code=Code,name=Name,amount=Amount,entry=Entry)
        Entrydata=project.Entrys.all()
        unique=project.Codes.all().order_by("-id")
        Codedata=[]
        seen_name=set()
        for item in unique:
            if item.code not in seen_name:
                Codedata.append(item)
            seen_name.add(item.code)
        Data={
            "User":name,
            "Project":Project,
            "Entry_data":Entrydata,
            "Code_data":Codedata,
        }
        return render(request,'Project.html',Data)

def Ledger_Page(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)
        unique=project.Entrys.all().order_by("id")
        Ledgerdata=[]
        seen_name=set()
        for item in unique:
            if item.name not in seen_name:
                Ledgerdata.append(item)
            seen_name.add(item.name)
        Data={
            "Project":Project,
            "Ledger":Ledgerdata,
        }
        return render(request,'Ledger.html',Data)

def TrialBalance_Page(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)
        Trial=TrialInfo.objects.filter(project=project)
        Drsum=0
        Crsum=0
        for item in Trial:
            if item.state == "DR":
                Drsum+=item.amount
            else:
                Crsum+=item.amount
        Data={
            "Project":Project,
            "Trial":Trial,
            "Drsum":Drsum,
            "Crsum":Crsum,
        }
        return render(request,'Trialbalance.html',Data)

def Stock_Page(request,Project):
    return render(request,'Stock.html',{"Project":Project})

def Account_Page(request,Account,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)
        unique=project.Entrys.filter(name=Account).order_by("id")
        Drsum=0
        Crsum=0
        Balance=0
        State="-"
        for item in unique:
            if item.entry == "DR":
                Drsum+=item.amount
            else:
                Crsum+=item.amount
        if Drsum>Crsum:
            Balance=Drsum-Crsum
            State="DR"
        else:
            Balance=Crsum-Drsum
            State="CR"
        try:
            Data=project.Trials.get(name=Account)
            Data.amount=Balance
            Data.state=State
            Data.save()
        except:
            project.Trials.create(project=project,name=Account,amount=Balance,state=State)
        return render(request,'Ledgerview.html',{"Account":Account,"Data":unique,"Balance":Balance,"State":State})

from django.shortcuts import render,redirect
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
                    TrialInfo.objects.filter(project=project,name=Name).delete()
                    DataInfo.objects.filter(project=project,name=Name).update(active=True)
            for i in range(5,9):
                if request.POST.get(f"Name{i}").strip():
                    Name=request.POST.get(f"Name{i}").strip().lower()
                    Amount=request.POST.get(f"Amount{i}")
                    Entry="CR"
                    DataInfo.objects.create(project=project,code=Code,name=Name,amount=Amount,entry=Entry)
                    TrialInfo.objects.filter(project=project,name=Name).delete()
                    DataInfo.objects.filter(project=project,name=Name).update(active=True)
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
        Trial=TrialInfo.objects.filter(project=project).order_by("order")
        Drsum=0
        Crsum=0
        Amount=0
        Tally=""
        for item in Trial:
            if item.state == "DR":
                Drsum+=item.amount
            else:
                Crsum+=item.amount
        if round(Drsum,2) == round(Crsum,2):
            Amount=Drsum
            Tally="Tally"
        else:
            Amount=Drsum-Crsum
            Tally="Difference"
        Data={
            "Project":Project,
            "Trial":Trial,
            "Amount":Amount,
            "Tally":Tally,
        }
        return render(request,'Trialbalance.html',Data)

def Stock_Page(request,Project):
    return render(request,'Stock.html',{"Project":Project})

def Account_Page(request,Account,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)
        Entry=project.Entrys.filter(name=Account).order_by("id")
        DataInfo.objects.filter(project=project,name=Account).update(active=False)
        Drsum=0
        Crsum=0
        Balance=0
        State=""
        for item in Entry:
            if item.entry=="DR" and State=="":
                State="DR"
            elif item.entry=="CR" and State=="":
                State="CR"
            if item.entry==State:
                Balance+=item.amount
                DataInfo.objects.filter(pk=item.id).update(ledgerbalance=Balance)
            else:
                Balance-=item.amount
                DataInfo.objects.filter(pk=item.id).update(ledgerbalance=Balance)
        Entry=project.Entrys.filter(name=Account).order_by("id")
        try:
            Data=project.Trials.get(name=Account)
            Data.amount=round(Balance,2)
            Data.state=State
            Data.save()
        except:
            project.Trials.create(project=project,name=Account,amount=round(Balance,2),state=State,order=Entry[0].id)
        return render(request,'Ledgerview.html',{"Account":Account,"Data":Entry,"Balance":Balance,"State":State})

def Delete_Page(request,Project,Code):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)
        Entry=project.Entrys.filter(code=Code)
        for item in Entry:
            TrialInfo.objects.filter(project=project,name=item.name).delete()
            DataInfo.objects.filter(project=project,name=item.name).update(active=True)
        Entry.delete()
        project.Codes.filter(code=Code).delete()
        return redirect('Journal',Project=Project)

def Editing_Page(request,Project,Code):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)
        Entry=project.Entrys.filter(code=Code)
        if request.POST:
            for item in Entry:
                Name=request.POST.get(f"Name{item.id}").strip().lower()
                Amount=float(request.POST.get(f"Amount{item.id}"))
                if item.name != Name or item.amount != Amount:
                    DataInfo.objects.filter(project=project,name=item.name).update(active=True)
                    DataInfo.objects.filter(pk=item.id).update(name=Name,amount=Amount)
                    DataInfo.objects.filter(project=project,name=Name).update(active=True)
                    TrialInfo.objects.filter(name=Name).delete()
                    TrialInfo.objects.filter(name=item.name).delete()
            return redirect('Journal',Project=Project)
        return render(request,'Editing.html',{"Entry":Entry,"Project":Project})

        

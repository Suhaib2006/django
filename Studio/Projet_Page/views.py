from django.shortcuts import render,redirect
from Home_Page.models import ProjectInfo
from .models import DataInfo,CodeInfo,TrialInfo,Questionpaper
from django.contrib.auth.models import User
from datetime import date
# Create your views here.

def Project_Page(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)
        Date=date.today().isoformat()
        error_msg=None
        if request.POST:
            Code=request.POST.get("Code").strip().upper()
            Create_date=request.POST.get("Date")
            Date=Create_date
            try:
                project.Codes.get(code=Code)
                error_msg= 'alerdy exist code'
            except:
                CodeInfo.objects.create(project=project,code=Code,date=Create_date)
            for i in range(1,5):
                if request.POST.get(f"Name{i}").strip() and request.POST.get(f"Amount{i}"):
                    Name=request.POST.get(f"Name{i}").strip().lower()
                    Amount=request.POST.get(f"Amount{i}")
                    Entry="DR"
                    DataInfo.objects.create(project=project,code=Code,name=Name,amount=Amount,entry=Entry,date=Create_date)
                    project.Trials.filter(project=project,name=Name).delete()
                    DataInfo.objects.filter(project=project,name=Name).update(active=True)
                    
            for i in range(5,9):
                if request.POST.get(f"Name{i}").strip() and request.POST.get(f"Amount{i}"):
                    Name=request.POST.get(f"Name{i}").strip().lower()
                    Amount=request.POST.get(f"Amount{i}")
                    Entry="CR"
                    DataInfo.objects.create(project=project,code=Code,name=Name,amount=Amount,entry=Entry,date=Create_date)
                    project.Trials.filter(project=project,name=Name).delete()
                    DataInfo.objects.filter(project=project,name=Name).update(active=True)
        Entrydata=project.Entrys.all().order_by("code","date")
        Codedata=project.Codes.all().order_by("-date","-id","-code")
        
        Data={
            "User":name,
            "Project":Project,
            "Entry_data":Entrydata,
            "Code_data":Codedata,
            "Date":Date,
            "codeactive":error_msg,
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
            "incomstatement":project.incomstatement,
        }
        return render(request,'Trialbalance.html',Data)

def Stock_Page(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)
        if request.POST:
            pdf_file=request.FILES.get('pdf')
            if pdf_file:
                Questionpaper.objects.create(project=project,pdf=pdf_file,uploaded=True)
        document=project.media.all()
        return render(request,'Stock.html',{"Project":Project,"Document":document})

#def Account_Page(request,Account,Project):
#    if request.user.is_authenticated:
#       name = request.user.username
#        user = User.objects.get(username=name)
#        project = ProjectInfo.objects.get(user=user,project=Project)
#       Entry=project.Entrys.filter(name=Account).order_by("date","id","code")
#       DataInfo.objects.filter(project=project,name=Account).update(active=False)
#       Drsum=0
#        Crsum=0
#       Balance=0
#        State=""
#       for item in Entry:
#            if item.entry=="DR" and State=="":
#                State="DR"
#            elif item.entry=="CR" and State=="":
#                State="CR"
#            if item.entry==State:
#                Balance+=item.amount
#                DataInfo.objects.filter(pk=item.id).update(ledgerbalance=Balance)
#           else:
#                Balance-=item.amount
#                if Balance<0:
#                    Balance*=(-1)
#                    if State=="DR":
#                        State="CR"
#                    else:
#                        State="DR"
#                DataInfo.objects.filter(pk=item.id).update(ledgerbalance=Balance)
#        Entry=project.Entrys.filter(name=Account).order_by("date","id","code")
#        try:
#            Data=project.Trials.get(name=Account)
#            Data.amount=round(Balance,2)
#           Data.state=State
#            Data.save()
#        except:
#            project.Trials.create(project=project,name=Account,amount=round(Balance,2),state=State,order=Entry[0].id)
#        return render(request,'Ledgerview.html',{"Account":Account,"Data":Entry,"Balance":Balance,"State":State})

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
        Date=project.Codes.get(code=Code)
        Date=Date.date.strftime('%Y-%m-%d')
        if request.POST:
            update_Date=request.POST.get("Date")
            for item in Entry:
                Name=request.POST.get(f"Name{item.id}").strip().lower()
                Amount=request.POST.get(f"Amount{item.id}")
                if Name=="" or Amount=="":
                    DataInfo.objects.filter(project=project,id=item.id).delete()
                    TrialInfo.objects.filter(name=item.name).delete()
                    DataInfo.objects.filter(project=project,name=item.name).update(active=True)
                else:
                    DataInfo.objects.filter(pk=item.id).update(date=update_Date)
                    CodeInfo.objects.filter(code=item.code).update(date=update_Date)
                    if item.name != Name or item.amount != float(Amount):
                        DataInfo.objects.filter(project=project,name=item.name).update(active=True)
                        DataInfo.objects.filter(pk=item.id).update(name=Name,amount=Amount)
                        DataInfo.objects.filter(project=project,name=Name).update(active=True)
                        TrialInfo.objects.filter(name=Name).delete()
                        TrialInfo.objects.filter(name=item.name).delete()

            return redirect('Journal',Project=Project)
        return render(request,'Editing.html',{"Entry":Entry,"Project":Project,"Date":Date})

        
def PdfDeleted(request,Project,Code):   
    Questionpaper.objects.get(pk=Code).delete()
    return redirect('Stock',Project=Project)

def AdditionalEntry(request,Project,Code): 
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        project = ProjectInfo.objects.get(user=user,project=Project)  

        if request.POST:
            Date=project.Codes.get(code=Code)
            Name=request.POST.get("Name").strip().lower()
            Amount=request.POST.get("Amount")
            Entry=request.POST.get("Entry").strip().upper()
            project.Entrys.create(project=project,code=Code,name=Name,amount=Amount,entry=Entry,active=True,date=Date.date)
            project.Trials.filter(project=project,name=Name).delete()
            project.Entrys.filter(name=Name).update(active=True)
        return redirect('Journal',Project=Project)
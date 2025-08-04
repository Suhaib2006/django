from django.http import JsonResponse
from Projet_Page.models import DataInfo
from Home_Page.models import ProjectInfo
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
import json
def OptionDataRead(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        getproject = ProjectInfo.objects.get(user=user,project=Project)
        getValue = request.GET.get('q')
        AllData=getproject.Entrys.filter(name__istartswith=getValue)
        UniqueData=[]
        seen_name=set()
        for item in AllData:
            if item.name not in seen_name:
                UniqueData.append(item.name)
            seen_name.add(item.name)
        
        return JsonResponse(list(UniqueData),safe=False)

def LedgerDataRead(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        getproject = ProjectInfo.objects.get(user=user,project=Project)
        getValue = request.GET.get('q')
        Alldata=getproject.Entrys.filter(name=getValue).order_by("date","id","code")
        getproject.Entrys.filter(project=getproject,name=getValue).update(active=False)
        Balance=0
        State=""
        for item in Alldata:
            print(item)
            if item.entry=="DR" and State=="":
                State="DR"
            elif item.entry=="CR" and State=="":
                State="CR"
            if item.entry==State:
                Balance+=item.amount
                getproject.Entrys.filter(pk=item.id).update(ledgerbalance=round(Balance,2))
            else:
                Balance-=item.amount
                if Balance<0:
                    Balance*=(-1)
                    if State=="DR":
                        State="CR"
                    else:
                        State="DR"
                getproject.Entrys.filter(pk=item.id).update(ledgerbalance=round(Balance,2))
        try:
            Data=getproject.Trials.get(name=getValue)
            Data.amount=round(Balance,2)
            Data.state=State
            Data.save()
        except:
            getproject.Trials.create(project=getproject,name=getValue,amount=round(Balance,2),state=State,order=Alldata[0].id)
        
        Alldata=getproject.Entrys.filter(name=getValue).order_by("date","id","code").values('id','date','name','amount','entry','ledgerbalance')
        return JsonResponse(list(Alldata),safe=False)

def StatementRead(request,Project):
    name = request.user.username
    user = User.objects.get(username=name)
    getproject = ProjectInfo.objects.get(user=user,project=Project)
    if(request.method == "POST"):
        data=json.loads(request.body)
        Name=data.get("Name")
        Statement=data.get("Statement")
        Type=data.get("Type")
        getproject.Trials.filter(name=Name).update(sheet=Statement,account_type=Type)
        
        return JsonResponse({"status":"Success uploaded"})
    
    return JsonResponse({"status":" uploading error please check"})
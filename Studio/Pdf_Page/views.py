from django.shortcuts import render,HttpResponse
from Projet_Page.models import DataInfo,ProjectInfo,CodeInfo
from django.contrib.auth.models import User
#pdf.py import
from .pdf import HtmlPdf
# Create your views here.

def Journal_Pdf(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        Username=User.objects.get(username=name)
        GetProject=ProjectInfo.objects.get(user=Username,project=Project)
        JournalEntry=GetProject.Entrys.all().order_by("code","-date")
        Codedata=GetProject.Codes.all().order_by("date","code")
        Data={
            "Project":Project,
            "Journal":JournalEntry,
            "Order":Codedata
        }
        pdf=HtmlPdf('JournalPdf.html',Data)
        return HttpResponse(pdf,content_type="application/pdf")
        #return render(request,'JournalPdf.html',Data)
def Ledger_Pdf(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        Username=User.objects.get(username=name)
        GetProject=ProjectInfo.objects.get(user=Username,project=Project)
        LedgerName=GetProject.Trials.all().order_by("order")
        LedgerData=GetProject.Entrys.all().order_by("date","code")
        Balance=0
        State=""
        for ItemName in LedgerName:
            for item in LedgerData:
                if ItemName.name==item.name:
                    if item.entry=="DR" and State=="":
                        State="DR"
                    elif item.entry=="CR" and State=="":
                        State="CR"
                    if item.entry==State:
                        Balance+=item.amount
                        DataInfo.objects.filter(pk=item.id).update(ledgerbalance=round(Balance,2))
                    else:
                        Balance-=item.amount
                        if Balance<0:
                            Balance*=(-1)
                            if State=="DR":
                                State="CR"
                            else:
                                State="DR"
                        DataInfo.objects.filter(pk=item.id).update(ledgerbalance=round(Balance,2))
            Balance=0
            State=""
        LedgerData=GetProject.Entrys.all().order_by("date","code")
        Data={
            "Project":Project,
            "Ledger":LedgerName,
            "TableData":LedgerData
        }
        pdf=HtmlPdf('LedgerPdf.html',Data)
        return HttpResponse(pdf,content_type="application/pdf")

def TrialBalance_Pdf(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        Username=User.objects.get(username=name)
        GetProject=ProjectInfo.objects.get(user=Username,project=Project)
        TrialData=GetProject.Trials.all().order_by("order")
        Tally=0
        for item in TrialData:
            if item.state == "CR":
                Tally+=item.amount

        Data={
            "Project":Project,
            "TrialData":TrialData,
            "Tally":Tally
        }
        #return render(request,'TrialBalancePdf.html',Data)
        pdf=HtmlPdf('TrialBalancePdf.html',Data)
        return HttpResponse(pdf,content_type="application/pdf")
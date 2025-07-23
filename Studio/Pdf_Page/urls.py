from django.urls import path
from . import views

urlpatterns = [
    path('Journal/',views.Journal_Pdf,name="JournalPdf"),
    path('Ledger/',views.Ledger_Pdf,name="LedgerPdf"),
    path('TrialBalance/',views.TrialBalance_Pdf,name="TrialBalancePdf"),
]
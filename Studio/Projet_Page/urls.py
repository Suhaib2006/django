from django.urls import path
from . import views
urlpatterns = [
    path('',views.Project_Page,name="Journal"),
    path('ledger/',views.Ledger_Page,name="Ledger"),
    path('trial/',views.TrialBalance_Page,name="TrialBalance"),
    path('stock/',views.Stock_Page,name="Stock"),
    path('ledger/<str:Account>/',views.Account_Page),
    path('Delete/<str:Code>/',views.Delete_Page),
    path('Editing/<str:Code>/',views.Editing_Page),
]
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.Project_Page,name="Journal"),
    path('ledger/',views.Ledger_Page,name="Ledger"),
    path('trial/',views.TrialBalance_Page,name="TrialBalance"),
    path('stock/',views.Stock_Page,name="Stock"),
    path('ledger/<str:Account>/',views.Account_Page),
    path('Delete/<str:Code>/',views.Delete_Page),
    path('Editing/<str:Code>/',views.Editing_Page),
    path('stock/<str:Code>/',views.PdfDeleted),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

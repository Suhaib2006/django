from . import views
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('Auth_Page.urls')),
    path('',include('Home_Page.urls')),
    path('Home/<str:Project>/',include('Projet_Page.urls')),
    path('Pdf/<str:Project>/',include('Pdf_Page.urls')),
    path('OptionData/<str:Project>/',views.OptionDataRead),
    path('LedgerData/<str:Project>/',views.LedgerDataRead),
    path('Statement/<str:Project>/',views.StatementRead),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
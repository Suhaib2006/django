
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('Auth_Page.urls')),
    path('',include('Home_Page.urls')),
    path('Home/<str:Project>/',include('Projet_Page.urls')),
] 
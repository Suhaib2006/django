
from django.urls import path
from . import views
urlpatterns = [
    path('',views.Login_Page,name="Login"),
    path('register/',views.Register_Page),
    path('logout/',views.Logout_Page),
]

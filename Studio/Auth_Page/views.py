from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def Login_Page(request):
    error_msg=None
    if request.POST:
        Username=request.POST['Username']
        Password=request.POST['Password']
        user=authenticate(username=Username,password=Password)
        if user:
            login(request,user)
            return redirect('Home')
        else:
            error_msg="User is not exist please create your account"
            return render(request,'Login.html',{"msg":error_msg})
    else:
        return render(request,'Login.html',{"msg":"Enter your informations"})

def Register_Page(request):
    error_msg=None
    if request.POST:
        Username=request.POST['Username']
        Email=request.POST['Email']
        Password=request.POST['Password']
        ConfirmPassword=request.POST['ConfirmPassword']
        try:
            if Username and Email and Password:
                if Password == ConfirmPassword:
                    user=User.objects.create_user(username=Username,email=Email,password=Password)
                    user.save()
                    return redirect('Login')
                else:
                    error_msg="Password not mached"
                    return render(request,'Register.html',{"msg":error_msg}) 
            else:
                error_msg="please enter all informations"
                return render(request,'Register.html',{"msg":error_msg}) 
        except Exception as e:
            print(e)
            error_msg="User_Name or Email  already exist "
            return render(request,'Register.html',{"msg":error_msg})   
    else:   
        return render(request,'Register.html',{"msg":"_"})      


def Logout_Page(request):
    logout(request)
    return redirect('Login')

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
#from rest_framework.views import APIView
from django.http import HttpResponse
'''
from .mailer import (
    send_reset_pwd_mail,
    send_feedback_mail
)
'''
from Mainapp import s, Entry
'''
def home(request):
    if(request.POST):
        
        contact_us_data = request.POST.dict()
        name = contact_us_data.get("name")
        email = contact_us_data.get("email")
        data = contact_us_data.get("text")
        #print(name, email, data)

        send_feedback_mail(email, name, data)
        
    return render(request, 'home.html')

'''
def login(request):
    if(request.POST):

        login_data = request.POST.dict()
        
        if(login_data.get("repeatpassword")):

            print("SIGNUP")
            name = login_data.get("name")
            email = login_data.get("email")
            password = login_data.get("password")
            repeat_password = login_data.get("repeatpassword")
            dob = login_data.get("dob")

            if Entry.check_user_exists(email):
                print("User already exists")
                return render(request, "login.html", {
                    'error' : "User Already Exists"
                    })

            else:
                if(password==repeat_password):
                    print("Password Match")
                    Entry.insert_user(name, email, password, dob)
                    print("Data Inserted Successfully")
                    return render(request, "login.html", {
                        'error' : "Sign Up Successful"
                        })

                else:
                    print("Password & Repeat Password DO NOT Match")
                    return render(request, "login.html", {
                        'error' : "Password & Repeat Password DO NOT Match"
                        })

        else:
            print("LOGIN")
            email = login_data.get("email")
            password = login_data.get("password")
            print("Email ID:", email, " & Password:", password)

            verif_login = Entry.check_hash(email,password)
            print(verif_login)

            if(Entry.check_hash(email, password)):
                print("Login Successful")
                return redirect("/")

            else:
                print("Login Failed")
                return render(request, "login.html", {
                    'error' : "Incorrect Login Credentials"
                    })
                
    else:
        if hasattr(s, 'error'):
            return render(request, "login.html", {'error': s.error})
        return render(request, "login.html")

'''
def reset_password_1(request):
    if(request.POST):

        print("PASSWORD RESET INIT")
        reset_data = request.POST.dict()
        email = reset_data.get("email")

        if(Entry.check_user_exists(email)):
            send_reset_pwd_mail(email)
            print("Mail sent to:", email)
            s.error = "We have sent you a mail to reset your password, Please check your inbox"
            return redirect("/login")
            # return render(request, "login.html", {
            #     'error' : "We have sent you a mail to reset your password, Please check your inbox"
            #     }) 
        
        else:
            print("User doesnt exist")
            return render(request, "reset_1.html", {
                'error' : "User doesn't exist"
                })
            
    return render(request, "reset_1.html")


def reset_password_2(request):
    if(request.POST):

        print("PASSWORD RESET FINAL")
        reset_data = request.POST.dict()
        password = reset_data.get("password")
        repeat_password = reset_data.get("repeatpassword")
        verif_code = reset_data.get("verif_code")
        verif_code = int(verif_code)
        
        if password==repeat_password:

            if Entry.check_verif_code(verif_code):
                print("Valid Verification code... Resetting Password")
                Entry.reset_password(password, verif_code)
                s.error = "Password reset successfully"
                return redirect("/login")
                # return render(request, "login.html", {'error' : "Password reset successfully"})

            else:
                print("Invalid Verification Code")
                return render(request, "reset_2.html", {
                    'error' : "Invalid Verification Code, Try Again"
                    })

        else:
            return render(request, "reset_2.html", {
                'error' : "Password & Repeat Password Don't Match"
                })

    return render(request, "reset_2.html")


'''
def index(Httpresponse):
    return HttpResponse('Hello you!')

'''
from django.contrib import admin
from django.urls import path
from django.urls.resolvers import URLPattern
from django.http import HttpResponse

from . import views

urlpatterns= [
    path('admin/', admin.site.urls),
    path('', views.login , name ='login.html')

    

]
'''






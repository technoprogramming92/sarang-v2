import json

from django.contrib import messages
from django.contrib.auth import logout, login
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_mgt_app.EmailBackEnd import EmailBackEnd


# Create your views here.


def showDemoPage(request):
    return render(request, "demo.html")


def ShowLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6Lf8MbchAAAAALDy8BA6mVWNHiLxBfVPZ9I6Nf-w"
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success']==False:
            messages.error(request, "Invalid Captcha Try Again")
            return HttpResponseRedirect("/")
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                return HttpResponseRedirect(reverse("student_home"))
            elif user.user_type == "4":
                return HttpResponseRedirect(reverse("warden_home"))

        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def getUserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + " User Type : " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

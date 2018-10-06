from django.shortcuts import render
from django.conf import settings
from .models import *
from django.views import *
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect,render_to_response
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate
from django.urls import reverse
from .forms import *
import csv
import codecs
import logging
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import requests
import os
from .all import final_score
import pandas as pd

@login_required
def upload_csv(request):
    data = {}
    k=0
    if "GET" == request.method:
        return render(request, 'screener/add_event.html', data)
    # if not GET, then proceed
    try:
        print("GHUSA")
        csv_file = request.FILES["csv_file"]
        print(csv_file)
        name = request.POST.get('name', '')
        print(name)
        if not csv_file.name.endswith('.csv'):
            print(1)
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("uploadcsv"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            print(2)
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("uploadcsv"))

        # file_data = csv_file.read().decode("utf-8")

        # lines = file_data.split("\n")

        i=0
        data_dict = {}
        data_dict["name"] = name
        try:
            form = EventForm(data_dict)
            print('------------------------------------------')
            # print(form.fields['created_by'])
            if form.is_valid():
                print(3)
                obj = form.save()
                obj.user = request.user
                obj.csv_file = csv_file
                obj.save()
                language = request.POST.get('language', '')
                skill = request.POST.get('skill', '')
                language = language.split(',')
                skill = skill.split(',')
                keywords = language+skill
                
                for keyw in keywords:
                    keyw.strip()
                    key = Keyword(word = keyw, event = obj)
                    key.save()
                k=1

                temp = [key.word for key in Keyword.objects.filter(event=obj)]
                temp = ",".join(temp)
                output_data = final_score(obj, temp)

            else:
                # print(form.errors)
                print(4)
                logging.getLogger("error_logger").error(form.errors.as_json())
        except Exception as e:
            print(5)
            logging.getLogger("error_logger").error(repr(e))
            pass


        # here github part
        # for line in lines:
        #     if i==0:
        #         i=1
        #         continue
        #     if line == '':
        #         break
        #     fields = line.split(",")
    except Exception as e:
        print(6)
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    if k==1:
        redirect_url = '/tables/' + str(obj.pk) + '/'
        return HttpResponseRedirect(redirect_url)
    return HttpResponseRedirect(reverse("uploadcsv"))


def email(request):
    subject = "You are IN"
    message = "Your registration for our event has been accepted. See you then !"
    from_email = settings.EMAIL_HOST_USER
    to_email = ['aayushkothari11@yahoo.com',settings.EMAIL_HOST_USER]
    send_mail(subject, message, from_email, to_email, fail_silently = False)
    return HttpResponse("done")


def login(request):
    if request.user.is_authenticated:
        print(0)
        redirect_url = '/events/'
        return HttpResponseRedirect(redirect_url)
    else:
        if request.method == 'POST':
            print(1)
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user:
                print(2)
                if user.is_active:
                    print(3)
                    redirect_url = '/events/'
                    auth_login(request, user)
                    return HttpResponseRedirect(redirect_url)
                else:
                    error = 'Your account is disabled.'
                    return render(request, 'screener/login.html', {'error': error})
            else:
                error = 'Incorrect Username or Password'
                return render(request, 'screener/login.html', {'error': error})
        else:
            return render(request, 'screener/login.html', {})


def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))

@login_required
def dashboard(request):
    return render(request, 'screener/dashboard.html')

@login_required
def user(request):
    return render(request, 'screener/user.html')

@login_required
def table(request,pk):
    if request.method == 'GET':
        event = Event.objects.get(pk=pk)
        applicants = Applicant.objects.filter(event=event)
        applicants = sorted(applicants, key=lambda x: x.score, reverse=True)
        return render(request, 'screener/table.html',{'applicants':applicants,'id':pk})
    else:
        number = request.POST.get('number','')
        print(number)
        print(type(number))
        numbers = int(number)
        event = Event.objects.get(pk=pk)
        applicants = Applicant.objects.filter(event=event)
        applicants = sorted(applicants, key=lambda x: x.score, reverse=True)
        applicants = applicants[0:numbers]
        to_email = []
        number = []
        for i in range(0,numbers):
            to_email.append(applicants[i].email)
            number.append(applicants[i].number)
        message = "Your registration has been accepted!!"
        key = '241331A8wh9vI5SO5bb7c684'
        for i in range(0,len(number)):
            urltosend = 'http://api.msg91.com/api/sendhttp.php?authkey=' + key + '&mobiles=' + str(number[i]) + '&message=' \
                + message + '&sender=MSGIND&route=4'
            print(urltosend)
            r = requests.get(urltosend)
            print(r.status_code)
        subject = "You are IN"
        message = "Your registration for our event has been accepted. See you then !"
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, to_email, fail_silently = False)
        return render(request, 'screener/table.html',{'applicants':applicants,'id':pk})

def send_sms(request):
    number = ["9920776239", "9619227299", "7977529093"]
    message = "Your registration has been accepted!!"
    key = '241331A8wh9vI5SO5bb7c684'
    for i in range(0,range(len(number))):
        urltosend = 'http://api.msg91.com/api/sendhttp.php?authkey=' + key + '&mobiles=' + number[i] + '&message=' \
            + message + '&sender=MSGIND&route=4'
        print(urltosend)
        r = requests.get(urltosend)
        print(r.status_code)
    return HttpResponse("done")


# export MSG91KEY="241331A8wh9vI5SO5bb7c684"
# copy past this line in env/bin/activate

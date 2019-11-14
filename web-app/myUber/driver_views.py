from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from .models import account, ride, driver
from django.core.mail import send_mail
import json

def hello(request, username):
    # RR = ride.objects.filter(driver=username).exclude(status='C')
    # if RR.count() != 0:
    #     context = {'username':username, 'list':RR}
    #     return render(request, "driverview.html", context)
    d = driver.objects.get(username=username)
    v_type = d.type;
    num = d.space
    info = d.special_info
    R = ride.objects.all()
    data = []
    for r in R:
        # print(r.v_type)
        # print(r.number)
        # print(r.special)
        # print(r.status)
        # print(r.special)
        if (r.v_type == '' or r.v_type == v_type) and (r.number+r.s_num <= num) and (info == r.special or r.special == 'None') and r.status == 'O':
            #print("1")
            data.append(r)
    context = {'username': username, 'list': data}
    return render(request, "driverpage.html", context)

def viewride(request, username):
    ID = int(request.POST['choice'])
    r1 = ride.objects.get(id=ID)
    d = driver.objects.get(username=username)
    if(r1.status != 'O'):
        v_type = d.type;
        num = d.space
        info = d.special_info
        R = ride.objects.all()
        data = []
        for r in R:
            if (r.v_type == '' or r.v_type == v_type) and (r.number <= num) and (
                    info == r.special or r.special == 'None') and r.status == 'O':
                data.append(r)
        context = {'username': username, 'list': data, 'error':'Sorry, another driver picked the ride, please refresh before select!'}
        return render(request, "driverpage.html", context)
    r1.status = 'D'
    r1.v_type = d.type
    r1.driver = username
    r1.save()
    r1
    context = {
        'username': username, 'list': r1}
    user1 = account.objects.get(username=r1.owner)
    user2 = account.objects.get(username=r1.driver)
    try:
        if r1.sharer != '' and r1.sharer != 'None' and r1.sharer is not None:
            user3 = account.objects.get(username=r1.sharer)
            send_mail(subject='confirmation from myUber',message='Hi, ' + user3.username + '. Your ride #' + str(ID) + ' has been confirmed!', from_email='myuberzy@gmail.com', recipient_list=[user3.email, ],fail_silently=False)
        send_mail(subject='confirmation from myUber', message='Hi, ' + user1.username + '. Your ride #' + str(ID) + ' has been confirmed!',from_email='myuberzy@gmail.com', recipient_list=[user1.email, ], fail_silently=False)
        send_mail(subject='confirmation from myUber',message='Hi, ' + user2.username + '. You has confirmed the ride #' + str(ID), from_email='myuberzy@gmail.com', recipient_list=[user2.email, ], fail_silently=False)
        return render(request, "driverview.html", context)
    except Exception:
        return render(request, "driverview.html", context)

def history(request, username):
    r = ride.objects.filter(driver=username, status='D')
    context = {'username':username, 'list':r}
    return render(request, "dhistory.html", context)

def complete(requst, username, id):
    ID = int(id)
    r = ride.objects.get(id=ID)
    r.status = 'C'
    r.save()
    return HttpResponseRedirect(reverse('driver', args=(username,)))

def edit(request, username):
    return render(request, "dedit.html", {'username':username})

def dretreive(request, username):
    ID = request.POST['choice']
    ID = int(ID)
    r = ride.objects.get(id=ID)
    context = {'username':username, 'list': r}
    return render(request, "driverview.html", context)

def updata(request, username):
    license = request.POST['license']
    type = request.POST['type']
    name = request.POST['name']
    number = request.POST['space']
    special = request.POST['special']
    r = ride.objects.filter(username=username, status='D')
    if r.count() != 0:
        return render(request, "dedit.html", {'username': username, 'message': 'Wrong! Edit after all rides complete'})
    d = driver.objects.get(username=username)
    if license != '':
        d.license = license
    if number != '':
        d.space = int(number)
    if name != '':
        d.name = name
    if type != '':
        d.type = type
    if special != '':
        d.special_info = special
    d.save()
    return render(request, "dedit.html", {'username': username, 'message':'Edit successfully'})

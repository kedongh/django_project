from django.shortcuts import render
from .models import account, driver
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

def usignup(request):
    return render(request, "usignup.html")

def dsignup(request):
    return render(request, "dsignup.html")

def ucreate(request):
    name = request.POST['username']
    passw = request.POST['password']
    email = request.POST['email']
    try:
        account.objects.get(pk=name)
    except(account.DoesNotExist):
        newuser = account(username=name, password=passw, email=email)
        newuser.save()
        return render(request, "Welcome.html")
    else:
        return render(request, 'usignup.html', {
            'error_message': 'Username is already used!',
        })

def dcreate(request):
    name = request.POST['username']
    passw = request.POST['password']
    realname = request.POST['name']
    type = request.POST['type']
    license = request.POST['license']
    space = request.POST['space']
    try:
        User = account.objects.get(pk=name)
    except(account.DoesNotExist):
        return render(request, 'dsignup.html', {
            'error_message2': 'Please create a account at first',
        })
    else:
        if(passw != User.password):
            return render(request, 'dsignup.html', {
                'error_message': 'Wrong password or username',
            })
    try:
        user = account(username=name, password=passw)
        driver.objects.get(user=user)
    except(driver.DoesNotExist):
        newdriver = driver(user=user, username=name, name=realname, type=type, license_number=license, space=space)
        newdriver.save()
        return render(request, "Welcome.html")
        # return HttpResponse('OK')
    else:

        return render(request, 'dsignup.html', {
            'error_message': 'You already is a myUber driver',
        })


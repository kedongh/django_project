from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import account,driver, ride
from django.urls import reverse

# Create your views here.
def ulogin(request):
    return render(request, 'ulogin.html')

def dlogin(request):
    return render(request, 'dlogin.html')

def ucheck(request):
    try:
        User = account.objects.get(pk=request.POST['username'])
    except(account.DoesNotExist):
        return render(request, 'ulogin.html', {
            'error_message': 'Password or username is wrong',
        })
    if User.password != request.POST['password']:
        return render(request, 'ulogin.html', {
            'error_message': 'Password or username is wrong',
        })
    else:
        name = request.POST['username']
        R = ride.objects.filter(owner=name).exclude(status='C')
        if R.count() == 0:
            RR = ride.objects.filter(driver=name).exclude(status='C')
            if RR.count() != 0:
                return render(request, 'ulogin.html', {
                    'error_message': 'You are a driver of an uncompleted ride',
                })
            R2 = ride.objects.filter(sharer=name).exclude(status='C')
            if R2.count() == 0:
                return HttpResponseRedirect(reverse('user', args=(name,)))
            else:
                if R2[0].status == 'O':
                    return HttpResponseRedirect(reverse('sretrieve', args=(name,)))
                else:
                    return HttpResponseRedirect(reverse('uview', args=(name,R2[0].id)))
        else:
            if R[0].status == 'O':
                return HttpResponseRedirect(reverse('uedit', args=(name, R[0].id)))
            else:
                return HttpResponseRedirect(reverse('uview', args=(name,R[0].id)))

def dcheck(request):
    username = request.POST['username']
    try:
        passw = request.POST['password']
        user = account.objects.get(pk=username)
    except(account.DoesNotExist):
        return render(request, 'dlogin.html', {
        'error_message': 'You do not have an account yet',
        })
    if user.password != passw:
        return render(request, 'dlogin.html', {
            'error_message': 'Password or username is wrong',
        })

    try:
        Account = account(username=username, password=passw)
        Driver = driver.objects.get(user=Account)
    except(driver.DoesNotExist):
        return render(request, 'dlogin.html', {
            'error_message': 'You are not a driver yet',
        })
    else:
        R1 = ride.objects.filter(owner=username).exclude(status='C')
        R2 = ride.objects.filter(sharer=username).exclude(status='C')
        if R1.count() != 0 or R2.count() != 0:
            return render(request, 'dlogin.html', {
                'error_message': 'You are currently a user of a ride',
            })
        username = request.POST['username']
        return HttpResponseRedirect(reverse('driver', args=(username,)))

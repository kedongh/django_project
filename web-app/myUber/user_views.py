from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from .models import account,driver,ride
from django.db.models import Q
import time, json

def hello(request, username, error1='', error2=''):
    context = {'username': username, 'error1': error1, 'error2':error2}
    return render(request, "userpage.html", context)

def searchride(request, username):
    time1 = request.POST['time1']
    # time1 = time.strptime(time1, '%H:%M')
    time2 = request.POST['time2']
    # time2 = time.strptime(time2, '%H:%M')
    dest = request.POST['dest']
    num = request.POST['num']
    info={'time1':time1, 'time2':time2, 'dest':dest, 'num':num}
    Ride = ride.objects.filter(dest=dest, shared=True)
    if Ride.count() == 0:
        context = {
        'error1' :'','error2':'no ride to the destination, maybe you can try again later', 'username':username
        }
        return render(request, 'userpage.html', context)
    else:
        list = []
        for r in Ride:
            at = str(r.arrive_t)
            if at > time1 and at < time2 and (r.sharer is None or r.sharer ==''):
                # r.sharer = username
                # r.number = r.number + num
                # r.save()
                list.append(r)
        if len(list) == 0:
            context = {
                'error1': '', 'error2': 'no ride matches the time, maybe you can try again later',
                'username': username
            }
            return render(request, 'userpage.html', context)
        context = {'username': username, 'list': list, 'info':info}
        return render(request, "sharerpage.html", context)

def requestride(request, username):
    dest = request.POST['dest']
    time = request.POST['time']
    num = request.POST['num']
    type = request.POST['type']
    share = request.POST['share']
    special = request.POST['special']
    # try:
    #     ride.objects.get(owner=username, status='O')
    # except(ride.DoesNotExist):
    newride = ride(dest=dest, arrive_t=time, special=special, shared=share, number=num, status='O', v_type=type,
                       owner=username)
    newride.save()
    return HttpResponseRedirect(reverse('uedit', args=(username, newride.id)))
    # else:
    #     context = {
    #         'error1': 'you already have a request', 'error2': '', 'username': username
    #     }
    #     return render(request, 'userpage.html', context)
def refreshride(request, username, time1, time2, num, dest):
    try:
        Ride = ride.objects.filter(dest=dest, shared=True)
    except(ride.DoesNotExist):
        error = 'no ride to the destination, maybe you can try again later'
        context = {'username': username, 'error1': '', 'error2': error}
        return render(request, "userpage.html", context)
    else:
        list = []
        for r in Ride:
            at = str(r.arrive_t)
            if at > time1 and at < time2 and r.sharer is None:
                # r.sharer = username
                # r.number = r.number + num
                # r.save()
                list.append(r)
        if len(list) == 0:
            error = 'no ride matches the arrive time, maybe you can try again later'
            context = {'username': username, 'error1': '', 'error2': error}
            return render(request, "userpage.html", context)
        info = {'time1': time1, 'time2': time2, 'dest': dest, 'num':num}
        context = {'username': username, 'list': list, 'info':info}
        return render(request, "sharerpage.html", context)

def uedit(request, username, id):
    r = ride.objects.get(id = int(id))
    return render(request, 'useredit.html', {'username': username, 'r': r})

def uchange(request, username, id):
    dest = request.POST['dest']
    atime = request.POST['time']
    number = request.POST['num']
    type = request.POST['type']
    special = request.POST['special']
    r = ride.objects.get(id=int(id))
    if r.status != 'O':
        error = 'You cannot edit, the ride is already confirmed'
        return render(request, 'useredit.html', {'username': username, 'r': r, 'error':error})
    if r.sharer != '' and r.sharer is not None:
        error = 'You cannot edit, a sharer joined in'
        return render(request, 'useredit.html', {'username': username, 'r': r, 'error': error})
    else:
        if dest == '' and atime == '' and number == '' and special == r.special and type == '':
            r.delete()
            return HttpResponseRedirect(reverse('user', args=(username,)))
        if dest != '':
            r.dest = dest
        if atime != '':
            r.arrive_t = atime
        if number != '':
            r.number = int(number)
        if special != '':
            r.special = special
        if type != '':
            r.v_type = type
        r.save()
        return render(request, 'useredit.html', {'username': username, 'r': r})

def utable(request, username):
    r = ride.objects.filter(Q(owner=username)|Q(sharer=username)).exclude(status='C')
    context={'username':username, 'list':r}
    return render(request, "uride.html", context)

def uride(request, username):
    ID = request.POST['choice']
    r = ride.objects.get(id=int(ID))
    if username==r.owner:
        return render(request, 'useredit.html', {'username': username, 'r': r})
    else:
        return render(request, "shareredit.html", {'username': username, 'r': r})


def uview(request, username, id):
    ID = int(id)
    r = ride.objects.get(id=ID)
    return render(request,'viewstatus.html', {'username': username, 'r': r})

def sretrieve(request, username):
    r = ride.objects.get(sharer=username, status='O')
    return render(request, "shareredit.html", {'username': username, 'r': r})

def sedit(request, username, num):
    ID = int(request.POST['choice'])
    r = ride.objects.get(id=ID)
    if(r.status != 'O'):
        context={'error1':'', 'error2':'sorry, the ride is closed, please try again', 'username':username}
        return render(request,"userpage.html",context)
    r.s_num = num
    r.sharer = username
    r.save()
    return render(request,"shareredit.html",{'username':username, 'r':r})

def scancel(request, username):
    r = ride.objects.get(sharer=username)
    if(r.status == 'O'):
        r.sharer = ''
        r.s_num = 0
        r.save()
        return render(request, "userpage.html", {'username':username})
    else:
        error = "The ride is confirmed, you cannot cancel it"
        context={'error':error, 'username':username, 'r': r}
        return render(request, "shareredit.html", context)


def query(request):
    ID = request.POST.get('ID')
    id = int(ID)
    row = ride.objects.get(id=id)
    # print(row.status)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps({'rows':row.status}))
    return response
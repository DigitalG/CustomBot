from django.shortcuts import render
from .models import *
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import logout as django_logout


# Create your views here.
def index(request):
    filters = Filter.objects.all()
    return render(request, 'index.html')


def filters(request):
    filter = Filter.objects.all()
    ctx = {'filters': filter}

    if request.method == 'POST':
        id = request.POST['FilterId']
        Filter.objects.get(pk=id).delete()

    return render(request, 'filters_page.html', ctx)


def create_filter(request):
    ctx = {}
    if request.method == 'POST':
        new_input = request.POST['Input']
        new_type = request.POST['Type']
        new_output = request.POST['Output']
        #new_name = ''
        if new_type == 'Replace':
            new_name = 'Replace {} with {}'.format(new_input, new_output)
        else:
            new_name = new_type + ' ' + new_input

        filter = Filter.objects.create(input=new_input,
                                       type=new_type,
                                       output=new_output,
                                       name=new_name)

    return render(request, 'create_filter.html', ctx)


def channels_list(request):
    channels = Channel.objects.all()
    ctx = {'channels': channels}

    if request.method == 'POST':
        id = request.POST['ChannelId']
        Channel.objects.get(pk=id).delete()

    return render(request, 'channels_list.html', ctx)


def add_channel(request):
    filters = Filter.objects.all()
    ctx = {'filters': filters}


    if request.method == 'POST':
        new_name = request.POST['Name']
        new_key = request.POST['Key']
        channel = Channel.objects.create(name=new_name,
                                         key=new_key)
        min = Filter.objects.all().order_by('id')[0].id
        max = Filter.objects.all().order_by('-id')[0].id
        for i in range(min, max):
            if request.POST['Check' + str(i)]:
                channel.filters.add(Filter.objects.filter(pk=i)[0])

        channel.save()

    return render(request, 'add_channel.html', ctx)


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/index')


def login(request):
    """Shows a login form and a registration link."""

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/index/")

        else:
            return HttpResponse("Invalid login. Please try again.")

    # if not POST then return login form
    return render(request, "login.html", {'next': ''})


def user_settings(request):

    return render(request, 'user_settings.html')
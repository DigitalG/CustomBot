from django.shortcuts import render
from .models import *
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import logout as django_logout
import os


# Technical functions
def check_dictionary():
    f = open('./channels.txt', 'r')
    arr = f.readlines()
    f.close()
    f = open('./channels.txt', 'w')
    lines = []
    IsNew = True
    for c in Channel.objects.all():
        for i in range(len(arr)):
            if c.key in arr[i]:
                IsNew = False
                break
        if IsNew:
            lines.append('{};0\n'.format(c.key))
        else:
            lines.append(arr[i])
    f.writelines(lines)
    f.close()


def check_admins():
    f = open('./admins.txt', 'r')
    arr = f.readlines()
    f.close()
    f = open('./admins.txt', 'w')
    lines = []
    IsNew = True
    for c in Channel.objects.all():
        for i in range(len(arr)):
            if c.key in arr[i]:
                IsNew = False
                break
        if IsNew:
            lines.append('{};0\n'.format(c.key))
        else:
            lines.append(arr[i])
    f.writelines(lines)
    f.close()


# Render functions
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
        key = Channel.objects.get(pk=id).key
        Channel.objects.get(pk=id).delete()

        check_dictionary()

    return render(request, 'channels_list.html', ctx)


def add_channel(request):
    filters = Filter.objects.all()
    ctx = {'filters': filters}

    if request.method == 'POST':
        new_name = request.POST['Name']
        new_key = request.POST['Key']
        new_forfilter = request.POST['ForFilter']
        if 'CheckCaption' in request.POST:
            keep = True
        else:
            keep = False

        channel = Channel.objects.create(name=new_name,
                                         key=new_key,
                                         forfilter=new_forfilter,
                                         KeepForwardedCaption=keep)
        if Filter.objects.all():
            min = Filter.objects.all().order_by('id')[0].id
            max = Filter.objects.all().order_by('-id')[0].id
            for i in range(min, max + 1):
                if 'Check' + str(i) in request.POST:
                    channel.filters.add(Filter.objects.filter(pk=i)[0])

        f = open('./channels.txt', 'r+')
        f.readlines()
        f.writelines([new_key + ';0\n'])
        f.close
        # check_dictionary()
        channel.save()
        return HttpResponseRedirect('/channels_list/')

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
    ctx = {}
    if request.method == 'POST':
        if 'TokenSubmit' in request.POST:
            TeleBot.objects.create(token=request.POST['token'])

        if 'ResetLogin' in request.POST:
            phone_number = Session.objects.all()[0].number
            os.remove('./{}.session'.format(phone_number))
            Session.objects.all()[0].delete()

        if 'ResetToken' in request.POST:
            TeleBot.objects.all()[0].delete()

    if TeleBot.objects.all().exists():
        ctx = {'IsToken': True,
               'token': TeleBot.objects.all()[0].token}
    else:
        ctx = {'IsToken': False}

    if Session.objects.all().exists():
        ctx['IsLogin'] = True
    else:
        ctx['IsLogin'] = False

    return render(request, 'user_settings.html', ctx)


def channel_details(request, id):
    channel = Channel.objects.filter(pk=id)[0]
    filters = channel.filters.all()
    ctx = {'channel': channel,
           'filters': filters}

    if request.method == 'POST':
        id = request.POST['FilterId']
        filters.get(pk=id).delete()

    return render(request, 'channel_details.html', ctx)


def edit_channel(request, id):
    channel = Channel.objects.filter(pk=id)[0]
    filters = Filter.objects.all()
    if request.method == 'POST':
        if Filter.objects.all():
            min = Filter.objects.all().order_by('id')[0].id
            max = Filter.objects.all().order_by('-id')[0].id
            for i in range(min, max + 1):
                if 'Check' + str(i) in request.POST:
                    channel.filters.add(Filter.objects.filter(pk=i)[0])
        new_name = request.POST['Name']
        new_key = request.POST['Key']
        new_forfilter = request.POST['ForFilter']
        if 'CheckCaption' in request.POST:
            keep = True
        else:
            keep = False
        old_key = channel.key
        channel.name = new_name
        channel.key = new_key
        channel.forfilter = new_forfilter
        channel.KeepForwardedCaption = keep
        channel.save()

        f = open('./channels.txt', 'r')
        lines = []
        arr = f.readlines()
        f.close()
        f = open('./channels.txt', 'w')
        IsNew = True
        for a in arr:
            if old_key in a:
                tmp = a.split(';')
                IsNew = False
                lines.append('{};{}'.format(new_key, tmp[1]))
            else:
                lines.append(a)
        if IsNew:
            lines.append('{};0\n'.format(new_key))

        f.writelines(lines)
        # check_dictionary()

        f.close()

        return HttpResponseRedirect('/channel_details/{}'.format(id))

    for f in filters:
        if f in channel.filters.all():
            filters = filters.exclude(name=f.name)

    OnlyText = False
    OnlyImages = False
    OnlyMImages = False
    OnlyMText = False
    Everything = False

    if channel.forfilter == 'Only Text':
        OnlyText = True
    elif channel.forfilter == 'Only Images':
        OnlyImages = True
    elif channel.forfilter == 'Only messages that include an image':
        OnlyMImages = True
    elif channel.forfilter == 'Only messages that include text':
        OnlyMText = True
    elif channel.forfilter == 'Everything':
        Everything = True

    ctx = {'filters': filters,
           'name': channel.name,
           'OnlyText': OnlyText,
           'OnlyImages': OnlyImages,
           'OnlyMImages': OnlyMImages,
           'OnlyMText': OnlyMText,
           'Everything': Everything,
           'KeepForwardedCaption': channel.KeepForwardedCaption,
           'key': channel.key}

    return render(request, 'edit_channel.html', ctx)


def tele_login(request):
    session = Session.objects.all()
    if session.exists():
        phone_number = session[0].number
        ctx = {'IsCode': True}
    else:
        ctx = {'IsCode': False}

    if request.method == 'POST':
        if session.exists():
            to_edit = session[0]
            to_edit.code = str(request.POST['Code'])
            to_edit.save()
            print(Session.objects.all()[0].code)
            return HttpResponseRedirect("/index")

        else:
            Session.objects.create(name='1',
                                   number=request.POST['PhoneNumber'],
                                   code='0')
            ctx = {'IsCode': True}
            return render(request, 'tele_login.html', ctx)

    return render(request, 'tele_login.html', ctx)


def admin_channels(request):
    channels = AdminChannel.objects.all()
    ctx = {'channels': channels}

    if request.method == 'POST':
        id = request.POST['ChannelId']
        key = AdminChannel.objects.get(pk=id).key
        AdminChannel.objects.get(pk=id).delete()

        check_admins()

    return render(request, 'admin_channels.html', ctx)


def add_admin(request):
    channel = AdminChannel.objects.all()
    ctx = {'channel': channel}

    if request.method == 'POST':
        new_name = request.POST['Name']
        new_key = request.POST['Key']

        channel = AdminChannel.objects.create(name=new_name,
                                              key=new_key)

        f = open('./admins.txt', 'r+')
        f.readlines()
        f.writelines([new_key + ';0\n'])
        f.close

        return HttpResponseRedirect('/admin_channels/')

    return render(request, 'add_admin.html', ctx)


def admin_details(request, id):
    channel = AdminChannel.objects.all()
    ctx = {'channel': channel}

    return render(request, 'channel_details.html', ctx)


def edit_admin(request, id):
    channel = AdminChannel.objects.all(id)[0]
    ctx = {'name': channel.name,
           'key': channel.key,
           'channel': channel}
    new_name = request.POST['Name']
    new_key = request.POST['Key']
    old_key = channel.key
    channel.name = new_name
    channel.key = new_key
    channel.save()




    return HttpResponseRedirect('/admin_details/{}'.format(id))
    return render(request, 'edit_admin.html', ctx)

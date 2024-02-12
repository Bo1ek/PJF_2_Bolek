import os
import calendar
from datetime import date, datetime, timedelta


from .utils import Calendar

import django.core.files.uploadedfile
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Topic, Message, CalendarEvent
from .forms import RoomForm, UserForm, CalendarEventForm
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.views import generic

 
def loginPage(request):
    page = 'login'
    # if user is logged in, he can't manually go to login_url adress. He will be redirected to home page
    if request.user.is_authenticated:
        return redirect('home')
 
 
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
 
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')
 
        user = authenticate(request, username=username, password=password)
 
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
            
 
    context = {'page': page}
    return render(request, 'base/login_register.html',context)
 
def logoutUser(request):
    logout(request)
    return redirect('home')
 
def registerPage(request):
    page = 'register'
    form = UserCreationForm()
 
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error had occured during registration')
        
    return render(request, 'base/login_register.html', {'form':form})
 
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
 
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q))                                
 
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
 
    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)
 
def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method =='POST':
        message = Message.objects.create(
        user=request.user,
        room=room,
        body=request.POST.get('comment')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
 
    file_name = request.GET.get('filename', '')
    if file_name:
        file_path = os.path.join('uploaded_files', file_name)
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
 
    if room.file.name:
        room_file_name = room.file.name.split('/')[1]
    else:
        room_file_name = ''
 
    context = {'room': room,'room_messages': room_messages, 'participants': participants, 'filename': room_file_name}
    return render(request, 'base/room.html',context)
 
def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_message': room_message, 'topics': topics}
    return render(request, 'base/profile.html', context)
 
 
@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
 
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
 
        if request.FILES:
            uploaded_file = request.FILES.get('uploaded_file')
        else:
            uploaded_file = ''
 
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            file = uploaded_file
        )
        return redirect('home')
 
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)
 
@login_required(login_url='/login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
 
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method =='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form,'topics': topics, 'room': room}
    return render(request,'base/room_form.html',context)
 
@login_required(login_url='/login')
def deleteRoom(request, pk):
    
    room = Room.objects.get(id=pk)
 
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
 
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)
 
@login_required(login_url='/login')
def deleteMessage(request, pk):
    
    message = Message.objects.get(id=pk)
 
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
 
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
 
@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
 
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, 'base/update-user.html', context)


class CalendarView(generic.ListView):
    model = CalendarEvent
    template_name = 'base/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required(login_url='/login')
def calendar_event(request, event_id=None):
    instance = CalendarEvent()
    if event_id:
        instance = get_object_or_404(CalendarEvent, pk=event_id)
    else:
        instance = CalendarEvent()

    form = CalendarEventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'base/calendar_event.html', {'form': form})

@login_required(login_url='/login')
def chat(request, *args, **kwargs):
    context = {}
    return render(request, "base/chat.html", context)
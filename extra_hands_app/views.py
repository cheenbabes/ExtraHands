from django.shortcuts import render
from django.http import HttpResponse
from extra_hands_app.models import Teacher, Client, Available_Time, Event, Email_List
from forms import EventForm, UserForm, TeacherForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
    context_dict={}
    response = render(request, 'base.html', context_dict)
    return response


def get_teacher(request, teacher_slug):
    context_dict ={}
    try:
        teacher = Teacher.objects.get(slug=teacher_slug)
        context_dict['teacher'] = teacher
    except Teacher.DoesNotExist:
        pass

    return render(request, 'teacher.html', context_dict)

def get_all_teachers(request):
    teachers = Teacher.objects.all()
    context_dict ={'teachers':teachers}
    response = render(request, 'teachers.html', context_dict)
    return response

def get_client(request, client_slug):
    context_dict = {}
    try:
        client = Client.objects.get(client_slug=client_slug)
        context_dict['client'] = client
    except Client.DoesNotExist:
        pass

    client_events = Event.objects.filter(client = client)
    context_dict['events'] = client_events

    return render(request, 'client.html', context_dict)

def get_all_clients(request):
    clients = Client.objects.all()
    context_dict = {'clients': clients}
    return render(request, 'clients.html', context_dict)

def add_event(request, client_slug):
    try:
        client = Client.objects.get(client_slug=client_slug)
    except Client.DoesNotExist:
        client = None

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            if client:
                event = form.save(commit=False)
                event.client = client
                event.save()
                url = reverse('get_client', kwargs={'client_slug': client_slug})
                return HttpResponseRedirect(url)
        else:
            print form.errors
    else:
        form = EventForm()

    context_dict = {'form': form, 'client': client}

    return render(request, 'add_event.html', context_dict)

def register_teacher(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        teacher_form = TeacherForm(data=request.POST)

        if user_form.is_valid() and teacher_form.is_valid():
            user= user_form.save()

            #hash the password
            user.set_password(user.password)
            user.save()

            teacher = teacher_form.save(commit=False)
            #associate the correct user profile with the teacher information
            teacher.user = user
            #save the teacher
            teacher.save()

            registered = True
        else:
            print user_form.errors, teacher_form.errors

    #GET Request
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()

    context_dict = {'user_form': user_form, 'teacher_form': teacher_form, 'registered': registered}

    return render(request, 'register_teacher.html', context_dict)









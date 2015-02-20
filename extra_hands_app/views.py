from django.shortcuts import render
from django.http import HttpResponse
from extra_hands_app.models import Teacher, Client, Available_Time, Event, Email_List
from forms import EventForm, UserForm, TeacherForm, ClientForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
                #url = reverse('get_client', kwargs={'client_slug': client_slug})
                return HttpResponseRedirect("/myaccount/")
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
            #Don't commit here because if the teacher info is bad it will
            #create a user but not a teacher
            user= user_form.save(commit=False)

            #hash the password
            user.set_password(user.password)
            user.save()

            teacher = teacher_form.save(commit=False)
            #associate the correct user profile with the teacher information
            teacher.user = user
            #save the teacher
            teacher.save()
            user.save()

            registered = True
        else:
            print user_form.errors, teacher_form.errors

    #GET Request
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()

    context_dict = {'user_form': user_form, 'teacher_form': teacher_form, 'registered': registered}

    return render(request, 'register_teacher.html', context_dict)


def register_client(request):
    registered = False

    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        client_form = ClientForm(data=request.POST)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)

            #hash the password
            user.set_password(user.password)
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()
            #now commit the user object that the client is saved
            user.save()

            registered = True
        else:
            print user_form.errors, client_form.errors

    #GET request
    else:
        user_form = UserForm()
        client_form = ClientForm()

    context_dict = {'user_form': user_form, 'client_form': client_form, 'registered': registered}

    return render(request, 'register_client.html', context_dict)

def user_login(request):

    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user= authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/myaccount/")
            else:
                #TODO make this another page with some kind of link to activate your account or something
                return HttpResponse("Your account is disabled")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            #probably want something better than just a blank http response page
            #TODO create an error page with another login box
            return HttpResponse("Invalid login details supplied")

    #GET Request, show the form
    else:
        return render(request, 'login.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


@login_required()
def my_account(request):
    user = request.user
    context_dict={'user':user}

    is_teacher = False
    is_client = False
    is_superuser = False

    if Teacher.objects.filter(user=user).exists():
        is_teacher = True
        teacher = Teacher.objects.filter(user=user)
        available_time = Available_Time.objects.filter(teacher=teacher)
        context_dict['times'] = available_time

    if Client.objects.filter(user=user).exists():
        is_client=True
        client = Client.objects.filter(user=user)
        client_events = Event.objects.filter(client=client)
        context_dict['events'] = client_events

    if user.is_superuser:
        is_superuser = True


    context_dict['is_teacher'] = is_teacher
    context_dict['is_superuser'] = is_superuser
    context_dict['is_client'] = is_client


    return render(request, "myaccount.html", context_dict)








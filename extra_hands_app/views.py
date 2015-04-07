from django.shortcuts import render
from django.http import HttpResponse
from extra_hands_app.models import Teacher, Client, Available_Time, Event, Email_List, Click
from forms import EventForm, UserForm, TeacherForm, ClientForm, AvailableTimeForm
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
import datetime
from decimal import Decimal
from dateutil.parser import parse as parse_date
import pytz
from templated_email import send_templated_mail



# Create your views here.

def index(request):
    context_dict={}
    response = render(request, 'base.html', context_dict)
    return response

#Allows a logged-in user to view a specific teacher profile.
@login_required
def get_teacher(request, teacher_slug):
    context_dict ={}
    try:
        teacher = Teacher.objects.get(slug=teacher_slug)
        context_dict['teacher'] = teacher
    except Teacher.DoesNotExist:
        pass

    return render(request, 'teacher.html', context_dict)

#View a list of teachers with links to their individual profiles.
@login_required
def get_all_teachers(request):
    teachers = Teacher.objects.all()
    context_dict ={'teachers':teachers}
    response = render(request, 'teachers.html', context_dict)
    return response

#Allows a logged in user to view details about a client. This will likely be decommissioned in the final app
@login_required
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

#List of all clients with links to their individual profiles. Will likely be removed.
@login_required
def get_all_clients(request):
    clients = Client.objects.all()
    context_dict = {'clients': clients}
    return render(request, 'clients.html', context_dict)

#First step for creating an event. Shows the Event form and posts the initial event information.
@login_required
def add_event(request, client_slug):
    try:
        client = Client.objects.get(client_slug=client_slug)
    except Client.DoesNotExist:
        client = None

    if request.user == client.user:
        if request.method == 'POST':
            form = EventForm(request.POST)

            if form.is_valid():
                if client:
                    event = form.save(commit=False)
                    event.client = client
                    event.save()
                    url = 'event/' + str(event.pk) +'/select-teacher/'
                    messages.success(request, "Initial creation of the event was successful. Please select teachers to email below.")

                    times_available = get_all_times_available_for_event(event)
                    for time in times_available:
                        if time.pk not in event.times_available and time.pk not in event.times_emailed:
                            event.times_available.extend([time.pk])
                    event.save()

                    return HttpResponseRedirect(url)
            else:
                print form.errors
        else:
            form = EventForm()

        context_dict = {'form': form, 'client': client}
        return render(request, 'add_event.html', context_dict)

    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

#Creates available time for a specific teacher.
@login_required
def add_time(request, teacher_slug):
    try:
        teacher = Teacher.objects.get(slug = teacher_slug)
    except Teacher.DoesNotExist:
        teacher = None
        return Http404("Teacher does not exist!")

    if request.user == teacher.user:
        if request.method == 'POST':
            #Check for double bookings
            if check_double_booked_time(teacher, request.POST.get('start_time'), request.POST.get('end_time')):
                messages.error(request, "This time is already booked or your times overlap! Please correct your entry and try again.")
                return HttpResponseRedirect("/teacher/" + teacher.slug + "/add_time/")
            #Create the form, validate, and save
            form = AvailableTimeForm(request.POST)
            if form.is_valid():
                if teacher:
                    time = form.save(commit=False)
                    time.teacher = teacher
                    time.save()
                    messages.success(request, "Your availability was added successfully.")
                    return HttpResponseRedirect("/myaccount/")
            else:
                print form.errors
        else:
            form = AvailableTimeForm()

        context_dict = {'form': form, 'teacher': teacher}
        return render(request, 'add_time.html', context_dict)
    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

#Allows a teacher to edit time they previously submitted
@login_required
def edit_time(request, time_pk):
    try:
        time = Available_Time.objects.get(pk=time_pk)
    except Available_Time.DoesNotExist:
        time = None
        dict ={'class_event': "alert-danger", 'message': "This scheduled time does not exist!", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)
    if request.user == time.teacher.user:
        if request.method == 'POST':
            form = AvailableTimeForm(request.POST)
            if form.is_valid():
                time.start_time = form.cleaned_data['start_time']
                time.end_time = form.cleaned_data['end_time']
                time.save()
                messages.success(request, "Your availability was updated successfully.")
                return HttpResponseRedirect("/myaccount/")
            else:
                print form.errors
        else:
            form = AvailableTimeForm(instance=time)
        context_dict = {'form': form, 'time':time}
        return render(request, 'edit_time.html', context_dict)
    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

#Allows a teacher or user to delete their own scheduled time objects
@login_required
def delete_time(request, time_pk):
    try:
        time = Available_Time.objects.get(pk=time_pk)
    except Available_Time.DoesNotExist:
        time = None
        dict ={'class_event': "alert-danger", 'message': "This scheduled time does not exist!", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)
    if request.user == time.teacher.user:
            time.delete()
            messages.success(request, "You have successfully deleted this time")
            return HttpResponseRedirect("/myaccount/")

    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

#Allows a client to edit an event they have created
@login_required
def edit_event(request, event_pk):
    event = Event.objects.get(pk=event_pk)

    if request.user == event.client.user:
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                event.start_time= form.cleaned_data['start_time']
                event.end_time = form.cleaned_data['end_time']
                event.comments = form.cleaned_data['comments']
                event.is_on_call = form.cleaned_data['is_on_call']
                # other editable fields go here
                event.save()
                messages.success(request, "Event was successfully edited.")
                return HttpResponseRedirect("/myaccount/")
            else:
                print form.errors
        else:
            form =EventForm(instance=event)
        context_dict ={'form': form, 'event': event}
        return render(request, 'edit_event.html', context_dict)

    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

@login_required
def delete_event(request, event_pk):
    try:
        event = Event.objects.get(pk= event_pk)
    except Event.DoesNotExist:
        event = None
        dict ={'class_event': "alert-danger", 'message': "This event does not exist!", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)
    if request.user == event.client.user:
        if event.in_progress or event.teacher is not None:
            messages.error(request, "This event is in progress and cannot be modified!")
            return HttpResponseRedirect("/myaccount/")
        else:
            event.delete()
            messages.success(request, "You have successfully deleted this event.")
            return HttpResponseRedirect("/myaccount/")
    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

#Renders the Registration form for a teacher if a GET and saves the teacher is a POST
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
            messages.success(request, "Thank you for registering! Welcome to your portal.")
            return HttpResponseRedirect("/myaccount/")
        else:
            print user_form.errors, teacher_form.errors

    #GET Request
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()

    context_dict = {'user_form': user_form, 'teacher_form': teacher_form, 'registered': registered}

    return render(request, 'register_teacher.html', context_dict)

#Renders the Client registration form for a GET and saves the client with a POST request
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
            messages.success(request, "Thank you for registering! Welcome to your portal.")
        else:
            print user_form.errors, client_form.errors

    #GET request
    else:
        user_form = UserForm()
        client_form = ClientForm()

    context_dict = {'user_form': user_form, 'client_form': client_form, 'registered': registered}

    return render(request, 'register_client.html', context_dict)

#Login page for the user
def user_login(request):

    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user= authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "You are logged in.")
                return HttpResponseRedirect("/myaccount/")
            else:
                dict ={'class_event': "alert-danger", 'message': "Your account is inactive. Contact the site administrator.", 'url': 'index', 'button_text': "Home" }
                return render(request, "generic_message.html", dict)
        else:
            messages.error(request, "You supplied incorrect login details. Please try again.")
            return HttpResponseRedirect("/login/")


    #GET Request, show the form
    else:
        return render(request, 'login.html', {})

#Log out the user and redirect them to the index
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    messages.success(request, "You are now logged out.")
    return HttpResponseRedirect('/')

#The main method for displaying the users information. The request is routed based on the type of user.
#For clients, they see a page with their upcoming and pending events.
#For teachers, they see a page with their confirmed events and available time calender
#The superuser sees all the events, clients, and teacher. Can be customized to be a dashboard for things that Django Admin can't do.
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
        available_time = Available_Time.objects.filter(teacher=teacher).filter(start_time__gte=datetime.datetime.today() - datetime.timedelta(days=1)).filter(active=True).order_by('start_time')
        events = Event.objects.filter(teacher=teacher).filter(start_time__gte=datetime.datetime.today() - datetime.timedelta(days=1)).order_by('start_time')
        context_dict['times'] = available_time
        context_dict['events'] = events

    if Client.objects.filter(user=user).exists():
        is_client=True
        client = Client.objects.filter(user=user)
        client_events_unconfirmed = Event.objects.filter(client=client).filter(teacher=None).filter(start_time__gte=datetime.datetime.today() - datetime.timedelta(days=1)).order_by('start_time')
        current_client_events = Event.objects.filter(start_time__gte=datetime.datetime.today() - datetime.timedelta(days=1)).exclude(teacher__isnull=True)

        for event in client_events_unconfirmed:
            times_available = get_all_times_available_for_event(event)
            for time in times_available:
                if time.pk not in event.times_available and time.pk not in event.times_emailed:
                    event.times_available.extend([time.pk])
            event.save()

        sum = 0
        for event in client_events_unconfirmed:
            sum += len(event.times_available)

        context_dict['notification_sum'] = sum
        context_dict['unconfirmed_events'] = client_events_unconfirmed
        context_dict['current_events'] = current_client_events

    if user.is_superuser:
        is_superuser = True
        context_dict['teachers'] = Teacher.objects.all()
        context_dict['clients'] = Client.objects.all()
        context_dict['events'] = Event.objects.all().order_by('start_time')



    context_dict['is_teacher'] = is_teacher
    context_dict['is_superuser'] = is_superuser
    context_dict['is_client'] = is_client
    context_dict['message'] = "You have successfully logged in."

    return render(request, "myaccount.html", context_dict)

#POST method for teachers to toggle their on-call status.
#The lack of the teacher URL param prevents this method from being toggled by anyone else and is harmless, redirecting the user's account
@login_required
def go_on_call(request):
    if request.method == 'POST':
        if Teacher.objects.filter(user=request.user).exists():
            teacher = Teacher.objects.get(user = request.user)
            #reverse whatever it is
            teacher.on_call = not teacher.on_call
            teacher.save()
            if teacher.on_call:
                messages.success(request, "You are now on call!")
            else:
                messages.warning(request, "You are not on call anymore!")
            return HttpResponseRedirect("/myaccount/")
        else:
            return HttpResponse("I have no idea how you got here")
    else:
        return HttpResponseRedirect("/myaccount/")

@login_required()
def change_time(request, teacher_pk):
    teacher = Teacher.objects.get(pk=teacher_pk)
    if request.user == teacher.user:
        if request.method =='POST':
            try:
                hours = Decimal(request.POST.get("hours"))
            except ValueError:
                messages.error(request, "Please enter a decimal value for hours between 0.5 and 3.")
                return HttpResponseRedirect("/myaccount/")
            if hours < 0.5 or hours > 3:
                messages.error(request, "Please enter a decimal value for hours between 0.5 and 3.")
                return HttpResponseRedirect("/myaccount/")
            else:
                teacher.time_between_events = hours
                teacher.save()
                messages.success(request, "Your time between events was successfully updated to %s hours" % hours)
                return HttpResponseRedirect('/myaccount/')

    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)


#Shows the available teachers for a particular event booking. Displays the teachers who have available times then and their profiles.
def show_available_teachers(request, event_pk):
    user = request.user
    context_dict={'user':user}

    event = Event.objects.get(pk=event_pk)
    context_dict['event'] = event

    if request.user == event.client.user:
        available_times =[]
        emailed_times =[]

        for time_pk in event.times_available:
            time = Available_Time.objects.get(pk=time_pk)
            available_times.append(time)

        for time_pk in event.times_emailed:
            time = Available_Time.objects.get(pk=time_pk)
            emailed_times.append(time)

        context_dict['emailed_times'] = emailed_times
        context_dict['times'] = available_times
        return render(request, 'select_teacher.html', context_dict)
    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

#Returns a list of available time given an event.
def get_all_times_available_for_event(event):
    times = Available_Time.objects.filter(active=True)
    available_times = []

    #This is the logic to only grab the times that match the criteria for starting at or before the event time and ending at or after the event.
    #The reason for grabbing the times and not the teachers is that each specific time has a teacher attached to it, but each teacher just has a list
    #of all the total times they have entered (which could be a lot and have no relevance)
    for time in times:
        if time.start_time <= event.start_time and time.end_time >= event.end_time:
            available_times.append(time)

    return available_times

#Given an event and a teacher, this method analyzes what to do with the available time that was assigned to the event.
#If there is more time left, the method creates new AvailableTime objects and assigns them to the teacher.
def get_times_to_deactivate(event, teacher):
    #all this code needs serious testing
    times = Available_Time.objects.filter(teacher=teacher)
    for time in times:
        #exact match
        if time.start_time == event.start_time and time.end_time == event.end_time:
            #set it to false and call it good
            time.active = False
            time.save()
        #available time start before event time and end time is the same
        if time.start_time < event.start_time and time.end_time == event.end_time:
            #check for the time delta and create new available time event
            delta = event.start_time - time.start_time
            time.active = False
            time.save()
            if(delta.seconds > 3600*teacher.time_between_events):
                new_time = Available_Time()
                new_time.start_time = time.start_time
                new_time.end_time = event.start_time - datetime.timedelta(hours=float(teacher.time_between_events))
                new_time.teacher = teacher
                new_time.save()
        #available time start is the same as event start time and end is after
        if time.start_time == event.start_time and time.end_time > event.end_time:
            #check for time delta
            delta = time.end_time - event.end_time
            time.active = False
            time.save()
            if(delta.seconds > 3600*teacher.time_between_events):
                new_time = Available_Time()
                new_time.start_time = event.end_time + datetime.timedelta(hours=float(teacher.time_between_events))
                new_time.end_time = time.end_time
                new_time.teacher = teacher
                new_time.save()
        #available time starts before event and ends after event
        if time.start_time < event.start_time and time.end_time > event.end_time:
            #check for time delta
            time.active= False
            time.save()
            delta_start = event.start_time - time.start_time
            delta_end = time.end_time - event.end_time

            if(delta_start.seconds > 3600*teacher.time_between_events):
                new_time = Available_Time()
                new_time.start_time = time.start_time
                new_time.end_time = event.start_time - datetime.timedelta(hours=float(teacher.time_between_events))
                new_time.teacher = teacher
                new_time.save()

            if(delta_end.seconds > 3600*teacher.time_between_events):
                new_time = Available_Time()
                new_time.start_time = event.end_time + datetime.timedelta(hours=float(teacher.time_between_events))
                new_time.end_time = time.end_time
                new_time.teacher = teacher
                new_time.save()

#Sends emails to the teachers that were selected by the client in the second part of the event creating process.
@login_required
def send_emails_to_teachers(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    subject = "{0} has just sent you an email about an event!".format(event.client.organization)
    return_address = "noreply@gmail.com"
    if request.user == event.client.user:
        if request.method == 'POST':
            #mark the event as in_progress and no longer available to be deleted
            event.in_progress = True
            #Loop through all available teachers and send out mail
            time_pks = request.POST.getlist('times')
            for pk in time_pks:
                time = Available_Time.objects.get(pk = pk)
                teacher = time.teacher
                name = teacher.user.get_full_name()
                link = "127.0.0.1:8000/confirm-event/{0}/{1}/".format(event.pk, teacher.pk)
                body = "Hi {0}! {1} has just created an event and they selected you as one of the candidates. Below is your individual link to confirm your participation in this event. " \
                       "When you click on this link, it will take to a another page where you will confirm your participation. Please do not share this link with anyone else. If you do not want to participate," \
                       "simply ignore this email." \
                       "Your link is {2}".format(name, event.client.organization, link)
                send_mail(subject, body, return_address, [teacher.user.email])

                #add this time to the emailed list so it cannot be emailed again.
                event.times_available.remove(int(pk))
                event.times_emailed.extend([int(pk)])
                event.save()

                print "This teacher's name is {0}, the primary key is {1}, and their email is {2}".format(teacher.user.get_full_name(), teacher.pk, teacher.user.email)
            messages.success(request, "Your email was sent successfully.")
            return HttpResponseRedirect("/myaccount/")

        else:
            dict ={'class_event': "alert-danger", 'message': "Something went wrong because you're not using this like you're supposed to.", 'url': 'myaccount', 'button_text': "My Account"}
            return render(request, "generic_message.html", dict)
    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

#Once a teacher clicks on their personal link, they are taken to this page to confirm that they want to commit to being in the event
@login_required
def confirm_teacher_part1(request, event_pk, teacher_pk):
    event = Event.objects.get(pk = event_pk)
    teacher = Teacher.objects.get(pk = teacher_pk)

    if request.user == teacher.user:
        #if the event already has a teacher
        if event.teacher is not None:
            #django won't do composite primary keys without fussing so I need to make my own and make sure duplicates don't exist
            if Click.objects.filter(teacher = teacher.pk).filter(event=event.pk).exists():
                dict={'class_event': "alert-warning", 'message': "You have already clicked on this event!", 'url': "myaccount", "button_text": "My Account"}
                return render(request, "generic_message.html", dict)
            else:
                #make a new click object
                click = Click()
                click.event = event.pk
                click.teacher = teacher.pk
                click.save()
                dict ={'class_event': "alert-warning", 'message': "Sorry, but this event has already been taken!", 'url': 'myaccount', 'button_text': "My Account"}
                return render(request, "generic_message.html", dict)

        context_dict = {'teacher': teacher, 'event': event}

        return render(request, 'teacher_event_confirm.html', context_dict)

    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

#Posts the final request and commit the teacher to the event
@login_required
def confirm_teacher_post(request, event_pk, teacher_pk):
    event = Event.objects.get(pk = event_pk)
    teacher = Teacher.objects.get(pk = teacher_pk)

    if request.user == teacher.user:
        if request.method == 'POST':
            #assign the event teacher to the teacher who clicked it.
            event.teacher=teacher
            event.save()

            #find all the times that the teacher has that will be marked inactive and mark them as inactive
            #run the method for splitting the times into new times and setting to false
            get_times_to_deactivate(event,teacher)

            #give the teacher a click
            click = Click()
            click.teacher = teacher.pk
            click.event = event.pk
            click.save()

            # send a confirmation email to the client
            # uncomment this when mail API is not blocked.
            # subject = "Your event has been filled by {0}!".format(teacher.user.get_full_name())
            # message = "{0} has successfully signed up for your event. You can find their details at {1}. If you have any questions, please reach out to them directly".format(teacher.user.get_full_name, "127.0.0.1:8000/teacher/{0}".format(teacher.slug))
            # from_email = "noreply@gmail.com"
            # recipient_list = [event.client.user.email]
            # send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "You successfully signed up for this event! Please make sure your availability was appropriately updated.")
            return HttpResponseRedirect("/myaccount/")

        else:
            dict ={'class_event': "alert-danger", 'message': "Something went wrong because you're not using this like you're supposed to.", 'url': 'myaccount', 'button_text': "My Account"}
            return render(request, "generic_message.html", dict)
    else:
        dict ={'class_event': "alert-danger", 'message': "You don't have permission to perform this action.", 'url': 'myaccount', 'button_text': "My Account"}
        return render(request, "generic_message.html", dict)

def generic_message(request):

    return render(request, "generic_message.html", {})


def check_double_booked_time(teacher, start_time, end_time):
    timezone = pytz.timezone('America/Denver')
    start_time_parse = timezone.localize(parse_date(start_time))
    end_time_parse = timezone.localize(parse_date(end_time))
    double_booked = False
    teacher_times = Available_Time.objects.filter(teacher = teacher)
    for time in teacher_times:
        if time.start_time <= start_time_parse <= time.end_time or time.start_time <= end_time_parse <= time.end_time:
            double_booked = True
            break

    return double_booked

def send_email_teacher(request, event_pk, teacher_pk):
    event = Event.objects.get(pk = event_pk)
    teacher = Teacher.objects.get(pk = teacher_pk)
    send_templated_mail(
        template_name='email_teacher',
        from_email='eugene.baibourin@gmail.com',
        recipient_list=[teacher.user.email],
        context={
            'event': event,
            'teacher': teacher
        },
    )

    messages.success(request, "Your email has been sent successfully to %s" % teacher.user.get_full_name())
    return HttpResponseRedirect("/myaccount/")




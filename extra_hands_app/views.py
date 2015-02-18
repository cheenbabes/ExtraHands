from django.shortcuts import render
from django.http import HttpResponse
from extra_hands_app.models import Teacher, Client, Available_Time, Event, Email_List

# Create your views here.

def index(request):
    context_dict = {'thing' : 'You made this work!'}
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

    return render(request, 'client.html', context_dict)

def get_all_clients(request):
    clients = Client.objects.all()
    context_dict = {'clients': clients}
    return render(request, 'clients.html', context_dict)




from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context_dict = {'thing' : 'You made this work!'}
    response = render(request, 'base.html', context_dict)
    return response

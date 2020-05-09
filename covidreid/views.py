from django.http import HttpResponse
from django.shortcuts import render
import datetime
from django.utils import timezone


# Index
def index(request):
    # Waiting for the functions
    return render(request, 'index.html')

def database(request):
    # Waiting for the functions
    return render(request, 'database.html')

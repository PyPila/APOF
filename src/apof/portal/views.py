from django.shortcuts import render


def index(request):
    return render(request, 'portal/index.html')

def login(request):
    return render(request, 'portal/login.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def login(request):
    return render(request, 'portal/login.html')


@login_required
def index(request):
    return render(request, 'portal/index.html')

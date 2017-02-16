from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def login(request):
    return render(request, 'portal/login.html')


@login_required
def index(request):
    return redirect('restaurant-list')

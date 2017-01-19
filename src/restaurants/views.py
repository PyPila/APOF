from django.shortcuts import render

from .models import Restaurant


def restaurants_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/index.html', {'restaurants': restaurants})

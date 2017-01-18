from django.shortcuts import render

from .models import Restaurant


def restaurants_list(request):
    """View for restaurants list."""
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/index.html', {'restaurants': restaurants})

from datetime import datetime

from django.db.models import Prefetch
from django.shortcuts import render

from .models import Restaurant, OpeningHours


def restaurants_list(request):
    restaurants = Restaurant.objects.all().prefetch_related('phonenumber_set')
    restaurants = restaurants.prefetch_related(
        Prefetch(
            'openinghours_set',
            queryset=OpeningHours.objects.filter(day=datetime.today().weekday()),
            to_attr='opening_hours'
        )
    )
    return render(request, 'restaurants/index.html', {'restaurants': restaurants})

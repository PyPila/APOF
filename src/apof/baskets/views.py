from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import datetime

from baskets.models import Basket, Order
from menus.models import Meal, Price


@login_required
def add_to_basket(request, meal_id, meal_price_id):
    meal_price = get_object_or_404(Price, pk=meal_price_id)
    meal = Meal.objects.get(pk=meal_id)
    basket, created = Basket.objects.get_or_create(
        owner=request.user,
        created_at=datetime.today()
    )
    Order.objects.create(meal=meal, size=meal_price.size, basket=basket)

    previous = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if previous:
        return previous
    return redirect('restaurant-list')

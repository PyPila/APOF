from __future__ import unicode_literals

from collections import defaultdict
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import datetime
from django.views.generic import ListView
from django.views.generic.edit import DeleteView

from apof.baskets.models import Basket, Order
from apof.menus.models import Meal, Price


class UserBasketView(LoginRequiredMixin, ListView):
    template_name = 'baskets/user_basket.html'
    model = Basket
    raise_exception = True

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', self.object_list)
        queryset = queryset.filter(owner=self.request.user)
        queryset = queryset.filter(created_at__lte=datetime.now())
        print queryset
        context = {
            'object_list': queryset
        }
        print context
        return context


class OrderListView(PermissionRequiredMixin, ListView):
    model = Order
    permission_required = ('baskets.delete_order', )
    raise_exception = True
    ordering = ('meal__menu__restaurant', )

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        queryset = kwargs.pop('object_list', self.object_list)
        restaurants_total_sum = defaultdict(Decimal)

        for order in queryset:
            restaurants_total_sum[order.get_restaurant_name()] += order.get_total_price()
        context['restaurants_total_sum'] = restaurants_total_sum

        return context


class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    model = Order
    permission_required = ('baskets.delete_order', )
    raise_exception = True
    success_url = reverse_lazy('order-list')


@login_required
def add_meal_to_basket(request, meal_id, meal_price_id):
    previous = request.META.get('HTTP_REFERER')
    meal_price = get_object_or_404(Price, pk=meal_price_id)
    meal = Meal.objects.get(pk=meal_id)
    basket, created = Basket.objects.get_or_create(
        owner=request.user,
        created_at=datetime.today()
    )
    Order.objects.create(meal=meal, size=meal_price.size, basket=basket)

    if previous:
        return HttpResponseRedirect(previous)
    return redirect('restaurant-list')

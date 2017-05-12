from __future__ import unicode_literals

from collections import defaultdict
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import datetime
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView

from apof.baskets.models import Basket, Order
from apof.menus.models import Meal, Price


class UserBasketView(LoginRequiredMixin, ListView):
    template_name = 'baskets/user_basket.html'
    model = Basket
    raise_exception = True

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', self.object_list)
        queryset = queryset.filter(owner=self.request.user)
        queryset = queryset.filter(created_at=datetime.today().date())
        basket_price = 0
        for basket in queryset:
            for order in basket.order_set.all():
                basket_price += order.get_total_price()
        context = {
            'object_list': queryset,
            'basket_price': basket_price
        }
        return context


class UserBasketConfirmationView(LoginRequiredMixin, UpdateView):
    model = Basket
    raise_exception = True
    fields = ['is_confirmed']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(UserBasketConfirmationView, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        if not obj.created_at == datetime.today().date():
            raise Http404
        return obj

    def post(self, args, **kwargs):
        self.object = self.get_object()
        if self.object.is_confirmed:
            self.object.is_confirmed = False
        else:
            self.object.is_confirmed = True
        self.object.save()
        return redirect('basket')


class UserBasketDeleteView(LoginRequiredMixin, DeleteView):
    model = Basket
    raise_exception = True
    success_url = reverse_lazy('basket')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(UserBasketDeleteView, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        if not obj.created_at == datetime.today().date():
            raise Http404
        return obj


class UserOrderQuantityUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    raise_exception = True
    fields = ['quantity']
    success_url = reverse_lazy('basket')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(UserOrderQuantityUpdateView, self).get_object()
        if not obj.basket.owner == self.request.user:
            raise Http404
        if not obj.basket.created_at == datetime.today().date():
            raise Http404
        return obj

    def post(self, args, **kwargs):
        self.object = self.get_object()
        self.object.quantity = self.request.POST['quantity']
        self.object.save()
        return redirect('basket')


class UserOrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    raise_exception = True
    success_url = reverse_lazy('basket')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(UserOrderDeleteView, self).get_object()
        if not obj.basket.owner == self.request.user:
            raise Http404
        if not obj.basket.created_at == datetime.today().date():
            raise Http404
        return obj


class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    model = Order
    permission_required = ('baskets.delete_order', )
    raise_exception = True
    success_url = reverse_lazy('order-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class OrderListView(PermissionRequiredMixin, ListView):
    model = Order
    permission_required = ('baskets.delete_order', )
    raise_exception = True
    ordering = ('meal__menu__restaurant', )

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        queryset = kwargs.pop('object_list', self.object_list)
        queryset = queryset.filter(basket__is_confirmed=True)
        context['object_list'] = queryset
        restaurants_total_sum = defaultdict(Decimal)

        for order in queryset:
            restaurants_total_sum[order.get_restaurant_name()] += order.get_total_price()
        context['restaurants_total_sum'] = restaurants_total_sum

        return context


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

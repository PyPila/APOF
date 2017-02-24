from __future__ import unicode_literals

from collections import defaultdict
from decimal import Decimal

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import DeleteView

from .models import Order


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

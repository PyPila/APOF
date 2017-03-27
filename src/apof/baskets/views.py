from collections import defaultdict
from decimal import Decimal
from django.db import models
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django.contrib.auth.models import User
from baskets.models import Basket

import datetime

class UserBasketView(LoginRequiredMixin, ListView):
    template_name = 'baskets/user_basket.html'
    model = Basket
    raise_exception = True

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', self.object_list)
        queryset = queryset.filter(owner=self.request.user)
        queryset = queryset.filter(created_at__lte=datetime.date(2017, 3, 27))
        print queryset
        context = {
            'object_list': queryset
        }
        print context
        return context

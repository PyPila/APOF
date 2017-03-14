from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from menus.models import Meal


class MealListView(LoginRequiredMixin, ListView):
    model = Meal
    context_object_name = 'meal_list'

    def get_queryset(self):
        queryset = super(MealListView, self).get_queryset()
        restaurant_pk = self.kwargs.get('restaurant_pk')

        if restaurant_pk:
            queryset = queryset.filter(menu__restaurant__pk=restaurant_pk)

        return queryset

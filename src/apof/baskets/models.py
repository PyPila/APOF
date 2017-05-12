from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from apof.menus.models import Meal, Size, Topping


ORDER_STATUS = (
    (0, 'Waiting'),
    (1, 'Canceled'),
    (2, 'Ordered'),
    (3, 'Delivered')
)


class Basket(models.Model):
    owner = models.ForeignKey(
        User,
        blank=False,
        null=True,
        on_delete=models.PROTECT,
        related_name='basket'
    )
    created_at = models.DateField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('owner', 'created_at')

    def __unicode__(self):
        return '{} {}'.format(self.__class__.__name__, self.owner.username)

    def __repr__(self):
        return '{} (Owner: {})'.format(self.__class__.__name__, self.owner)


class Order(models.Model):
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    meal = models.ForeignKey(Meal, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    toppings = models.ManyToManyField(Topping, blank=True)
    quantity = models.IntegerField(blank=True, default=1)
    basket = models.ForeignKey(Basket, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return '{} {}'.format(self.basket.owner, self.meal.name)

    def __repr__(self):
        return '{} (Basket: {}, Restaurant: {}, Meal: {})'.format(
            self.__class__.__name__,
            self.basket.pk,
            self.meal.menu.restaurant,
            self.meal.name
        )

    def get_restaurant_name(self):
        return self.meal.menu.restaurant.name

    def get_price(self):
        meal_price = self.meal.prices.values('value').get(size=self.size)
        toppings = self.toppings.filter(prices__size=self.size)
        toppings_price = toppings.aggregate(Sum('prices__value'))
        total_price = meal_price['value']
        if toppings_price['prices__value__sum']:
            total_price += toppings_price['prices__value__sum']
        return total_price

    def get_total_price(self):
        return self.get_price() * self.quantity

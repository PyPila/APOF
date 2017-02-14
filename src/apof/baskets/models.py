from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from menus.models import Meal, Size, Topping


ORDER_STATUS = (
    (0, 'Waiting'),
    (1, 'Canceled'),
    (2, 'Ordered'),
    (3, 'Delivered')
)


class Basket(models.Model):
    owner = models.ForeignKey(User, blank=False, null=True, on_delete=models.PROTECT)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('owner', 'created_at')

    def __unicode__(self):
        return '{} {}'.format(self.__class__.__name__, self.owner.username)

    def __repr_(self):
        return '{} (Owner: {})'.format(self.__class_.__name__, self.owner)


class Order(models.Model):
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    meal = models.ForeignKey(Meal, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    toppings = models.ManyToManyField(Topping, blank=True)
    quantity = models.IntegerField(blank=True, default=1)
    basket = models.ForeignKey(Basket, blank=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return '{} {} {}'.format(self.basket.owner, self.meal, self.created_at)

    def __repr_(self):
        return '{} (Basket {}, Meal: {}, Created at: {})'.format(
            self.__class__.__name__,
            self.basket.pk,
            self.meal,
            self.created_at
        )

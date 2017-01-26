from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    def __unicode__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, blank=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return '{}'.format(self.restaurant)


class Size(models.Model):
    menu = models.ForeignKey(Menu, blank=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=50, blank=True, unique=True, default='Normal size')
    value = models.DecimalField(max_digits=3, decimal_places=0, blank=True)
    value_unit = models.CharField(max_length=15, blank=True)

    class Meta:
        unique_together = ('menu', 'value', 'value_unit')

    def __unicode__(self):
        if self.value and self.value_unit:
            return '{} ({} {})'.format(self.description, self.value, self.value_unit)
        else:
            return self.description


class Meal(models.Model):
    menu = models.ForeignKey(Menu, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    ingredients = models.ManyToManyField('Ingredient', blank=True)

    prices = GenericRelation('Price')

    def __unicode__(self):
        return '{} | {}'.format(self.menu, self.name)


class Topping(models.Model):
    menu = models.ForeignKey(Menu, blank=False, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', blank=True, on_delete=models.PROTECT)

    prices = GenericRelation('Price')

    class Meta:
        unique_together = ('menu', 'ingredient')

    def __unicode__(self):
        return '{} | {}'.format(self.menu, self.ingredient)


class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True)

    def __unicode__(self):
        return self.name


class Price(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    size = models.ForeignKey(Size, blank=False, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return str(self.value)

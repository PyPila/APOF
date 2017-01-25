from __future__ import unicode_literals

from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    def __unicode__(self):
        return self.name

class Menu(models.Model):
    restaurant =  models.OneToOneField(Restaurant, blank=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return '{} {}'.format(self.restaurant, 'menu')

class MealCategory(models.Model):
    menu = models.ForeignKey(Menu, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)

    class Meta:
        unique_together = ('name', 'menu')

    def __unicode__(self):
        return '{} --> {}'.format(self.menu, self.name)

class Meal(models.Model):
    category = models.ForeignKey(MealCategory, blank=False)
    name = models.CharField(max_length=150, blank=False)

    def __unicode__(self):
        return self.name

class Size(models.Model):
    category = models.ForeignKey(MealCategory, blank=False)
    description = models.CharField(max_length=50, blank=True, unique=True, default='Normal size')
    value = models.DecimalField(max_digits=3, decimal_places=0, blank=True)
    value_unit = models.CharField(max_length=15, blank=True)
    meal = models.ManyToManyField(Meal, blank=True)

    class Meta:
        unique_together = ('value', 'value_unit', 'category')

    def __unicode__(self):
        return '{} {} ({} {})'.format(self.category, self.description, self.value, self.value_unit)

class MealPrice(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    size = models.ForeignKey(Size, blank=False)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, blank=False)

    def __unicode__(self):
        return '{} {}'.format(self.size, self.value)



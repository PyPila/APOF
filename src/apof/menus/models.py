from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apof.restaurants.models import Restaurant


class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, blank=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.restaurant.name

    def __repr__(self):
        return '{}(Restaurant: {})'.format(self.__class__.__name__, self.restaurant.name)


class Size(models.Model):
    menu = models.ForeignKey(Menu, blank=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=50, blank=True, default='Normal size')
    value = models.DecimalField(max_digits=3, decimal_places=0, blank=True)
    value_unit = models.CharField(max_length=15, blank=True)

    class Meta:
        unique_together = ('menu', 'value', 'value_unit')

    def __unicode__(self):
        if self.value and self.value_unit:
            return '{} ({} {})'.format(self.description, self.value, self.value_unit)
        else:
            return self.description

    def __repr__(self):
        return '{}(Menu: {}, Value: {}{})'.format(
            self.__class__.__name__,
            self.menu,
            self.value,
            self.value_unit
        )


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '{}(Name: {})'.format(
            self.__class__.__name__,
            self.name
        )


class Meal(models.Model):
    menu = models.ForeignKey(Menu, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    ingredients = models.ManyToManyField('Ingredient', blank=True)
    prices = GenericRelation('Price')
    logo = models.ImageField(
        blank=True,
        upload_to='meals/',
        default='/meals/meal_default.jpeg'
    )
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('menu', 'name')

    def __unicode__(self):
        return '{} | {}'.format(self.menu, self.name)

    def __repr__(self):
        return '{}(Menu: {}, Name: {})'.format(
            self.__class__.__name__,
            self.menu,
            self.name
        )


class Topping(models.Model):
    menu = models.ForeignKey(Menu, blank=False, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', blank=True, on_delete=models.PROTECT)
    prices = GenericRelation('Price')

    class Meta:
        unique_together = ('menu', 'ingredient')

    def __unicode__(self):
        return '{} | {}'.format(self.menu, self.ingredient)

    def __repr__(self):
        return '{}(Menu: {}, Igredient: {})'.format(
            self.__class__.__name__,
            self.menu,
            self.ingredient
        )


class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '{}(Name: {})'.format(self.__class__.__name__, self.name)


class Price(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    size = models.ForeignKey(Size, blank=False, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return str(self.value)

    def __repr__(self):
        return '{}(Value: {}, Object: {})'.format(
            self.__class__.__name__,
            self.value,
            self.content_object
        )

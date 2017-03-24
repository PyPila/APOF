from __future__ import unicode_literals

from django.db import models


WEEKDAYS = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday')
]


class Restaurant(models.Model):
    name = models.CharField(blank=False, max_length=50, unique=True)
    logo = models.ImageField(blank=False, upload_to='logos/')
    website = models.URLField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '{}(Name: {})'.format(self.__class__.__name__, self.name)

    def get_phone_numbers(self):
        return [phone_number.number for phone_number in self.phonenumber_set.all()]


class OpeningHours(models.Model):
    restaurant = models.ForeignKey('Restaurant')
    day = models.IntegerField(blank=False, choices=WEEKDAYS)

    opening_from = models.TimeField(blank=False, verbose_name='Open from')
    opening_to = models.TimeField(blank=False, verbose_name='Open to')

    ordering_from = models.TimeField(blank=True, null=True, verbose_name='Ordering from')

    class Meta:
        unique_together = ('restaurant', 'day')
        verbose_name_plural = "opening hours"
        ordering = ['restaurant', 'day']

    def __unicode__(self):
        return '{} | {} | {:%H:%M} | {:%H:%M}'.format(
            self.restaurant,
            self.get_day_display(),
            self.opening_from,
            self.opening_to
        )

    def __repr__(self):
        return '{}(Restaurant: {}, Day: {})'.format(
            self.__class__.__name__,
            self.restaurant.name,
            self.day
        )


class PhoneNumber(models.Model):
    restaurant = models.ForeignKey('Restaurant')
    number = models.CharField(blank=False, max_length=10, unique=True)

    def __unicode__(self):
        return '{} | {}'.format(self.restaurant, self.number)

    def __repr__(self):
        return '{}(Restaurant: {}, Number: {})'.format(
            self.__class__.__name__,
            self.restaurant.name,
            self.number
        )

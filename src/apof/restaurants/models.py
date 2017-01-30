from __future__ import unicode_literals

from django.db import models


class Restaurant(models.Model):
    name = models.CharField(blank=False, max_length=50, unique=True)
    logo = models.ImageField(blank=False, upload_to='logos/')

    def __unicode__(self):
        return self.name


WEEKDAYS = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
]


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


class PhoneNumber(models.Model):
    restaurant = models.ForeignKey('Restaurant')
    number = models.CharField(blank=False, max_length=10, unique=True)

    def __unicode__(self):
        return '{} | {}'.format(self.restaurant, self.number)

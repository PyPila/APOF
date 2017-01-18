from __future__ import unicode_literals

from django.db import models


class Restaurant(models.Model):
    """Restaurant model"""
    name = models.CharField(blank=False, max_length=50, unique=True)
    logo = models.ImageField(blank=False, upload_to='logos/')
    opening = models.CharField(
        blank=False,
        max_length=100,
        verbose_name='Opening hours',
    )

    def __str__(self):
        return self.name

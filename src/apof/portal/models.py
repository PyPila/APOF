from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    avatar = models.ImageField(
        max_length=140,
        blank=True,
        upload_to='avatars/',
        default='avatars/base.jpg',
    )

    def get_avatar(self):
        return self.avatar.url

    def __unicode__(self):
        return 'Profile of user: {}'.format(self.user.username)

    def __repr__(self):
        return '{}(User: {}, Avatar: {})'.format(
            self.__class__.__name__,
            self.user.username,
            self.avatar
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    if kwargs.get('created'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()

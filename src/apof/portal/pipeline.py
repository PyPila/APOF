import urllib2
import os
from django.conf import settings
from django.core.files.base import ContentFile


def get_avatar(backend, strategy, response, user=None, *args, **kwargs):
    url = None

    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
    if hasattr(user, 'profile'):
        avatar = user.profile.avatar
    if url:
        ext = url.split('.')[-1]
        if avatar.url != os.path.join(settings.MEDIA_URL, 'avatars/base.jpg'):
            avatar.delete()
        user.profile.avatar.save(
            '{0}.{1}'.format('avatar', ext),
            ContentFile(urllib2.urlopen(url).read()),
            save=False
        )
        user.save()

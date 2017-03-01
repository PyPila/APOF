import urllib2

from django.core.files.base import ContentFile


def get_avatar(backend, strategy, response, user=None, *args, **kwargs):
    url = None

    if backend.name == 'google-oauth2':
        url = response['image'].get('url')

    if url:
        avatar = user.profile.avatar
        ext = url.split('.')[-1]

        if avatar.url != '/media/avatars/base.jpg':
            avatar.delete()
        user.profile.avatar.save(
            '{0}.{1}'.format('avatar', ext),
            ContentFile(urllib2.urlopen(url).read()),
            save=False
        )
        user.save()

def get_avatar(backend, strategy, response, user=None, *args, **kwargs):
    url = None
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
    if url:
        prof = user.profile
        prof.avatar = url
        user.save()

from social_auth.backends.facebook import FacebookBackend
from social_auth.backends import google

def handle_new_user(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
 
    elif backend.__class__ == TwitterBackend:
        url = response.get('profile_image_url', '').replace('_normal', '')
 
    if url:
        profile = user.get_profile()
        profile.image = url
        print response['email']
        profile.email = response['email']
        profile.save()

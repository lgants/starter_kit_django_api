from main.users.models import UserProfile, AuthGithub
from main.helpers import update_or_create


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user.get_profile()
        if profile is None:
            profile = Profile(user_id=user.id)
        profile.gender = response.get('gender')
        profile.link = response.get('link')
        profile.timezone = response.get('timezone')
        profile.save()

    if backend.name == 'github':
        profile_instance = user.profile or UserProfile()
        update_or_create(profile_instance, {
            'user': user,
            'avatar_url': response.get('avatar_url', None),
            'bio': response.get('bio', None),
            'first_name': None,
            'last_name': None
        })

        auth_github_instance = user.auth_github or AuthGithub()
        update_or_create(auth_github_instance, {
            'user': user,
            'gh_id': response.get('id'),
            'display_name': response.get('login'),
            'response': response.__str__()
        })

    if backend.name == 'gitlab':
        # TODO: implement condition
        pass

    if backend.name == 'bitbucket':
        # TODO: implement condition
        pass

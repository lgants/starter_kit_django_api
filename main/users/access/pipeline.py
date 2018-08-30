from main.users.models import UserProfile, AuthGithub

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
        if hasattr(user, 'profile') and user.profile is not None:
            UserProfile.objects.create(
                user=user,
                avatar_url=response.get('avatar_url', None),
                bio=response.get('bio', None),
                first_name=None,
                last_name=None
            )

        if hasattr(user, 'auth_github') and user.auth_github is not None:
            AuthGithub.objects.create(
                user=user,
                gh_id=response.get('id'),
                display_name=response.get('login'),
                response=response.__str__()
            )

    if backend.name == 'gitlab':
        # TODO: implement condition
        pass

    if backend.name == 'bitbucket':
        # TODO: implement condition
        pass

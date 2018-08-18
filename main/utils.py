def get_authorization_header(request):
    # import pdb; pdb.set_trace()
    auth = request.META.get('HTTP_AUTHORIZATION', '').split()
    # auth = request.META.get(jwt_settings.JWT_AUTH_HEADER, '').split()
    # prefix = jwt_settings.JWT_AUTH_HEADER_PREFIX

    # if len(auth) != 2 or auth[0].lower() != prefix.lower():
    if len(auth) != 2:
        return None
    return auth[1]

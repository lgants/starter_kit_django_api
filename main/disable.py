class DisableCSRF(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
            # Code to be executed for each request before
            # the view (and later middleware) are called.

            # NOTE: this is bad/unsecure; change to apply only if DEBUG=True and avoid csrf in deploy architecture with reverse proxies
            setattr(request, '_dont_enforce_csrf_checks', True)

            response = self.get_response(request)

            # Code to be executed for each request/response after
            # the view is called.

            return response

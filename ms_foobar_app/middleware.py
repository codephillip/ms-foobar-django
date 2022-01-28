from django.utils.deprecation import MiddlewareMixin

# NOTE: This is not best practise, however, api requests from some browser would fail continuous so explains the use
# of this. Enhance this CSRF solution if necessary

class DisableCsrfCheck(MiddlewareMixin):
    def process_request(self, req):
        attr = '_dont_enforce_csrf_checks'
        if not getattr(req, attr, False):
            setattr(req, attr, True)

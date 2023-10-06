# middleware.py

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class CsrfExemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Apply csrf_exempt to all Django admin views
        if request.path.startswith('/admin/'):
            view_func = method_decorator(csrf_exempt)(view_func)
        return None

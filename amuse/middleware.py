from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout

class BruteForceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.session.setdefault('login_attempts', 0)

        response = self.get_response(request)

        if request.user.is_authenticated and response.status_code == 200:
            login_attempts = request.session.get('login_attempts', 0)
            if login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                logout(request)
                messages.error(request, "Your account is temporarily locked. Please try again later.")
            elif response.context_data.get('invalid_login', False):
                request.session['login_attempts'] = login_attempts + 1
            else:
                request.session['login_attempts'] = 0

        return response

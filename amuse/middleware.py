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
            request.session.setdefault('last_login_attempt', None)

        response = self.get_response(request)

        if request.user.is_authenticated and response.status_code == 200:
            login_attempts = request.session.get('login_attempts', 0)
            last_login_attempt = request.session.get('last_login_attempt')
            if login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                if last_login_attempt is not None and \
                        timezone.now() < last_login_attempt + timezone.timedelta(seconds=settings.LOCKOUT_TIME):
                    # Still within lockout time, logout user
                    logout(request)
                    messages.error(request, "Your account is temporarily locked. Please try again later.")
                else:
                    # Reset login attempts and last login attempt time
                    request.session['login_attempts'] = 0
                    request.session['last_login_attempt'] = None
            elif 'invalid_login' in request.POST:
                request.session['login_attempts'] = login_attempts + 1
                request.session['last_login_attempt'] = timezone.now()
            else:
                request.session['login_attempts'] = 0
                request.session['last_login_attempt'] = None

        return response

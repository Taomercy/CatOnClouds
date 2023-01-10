import functools

from django.shortcuts import render
from django.views.decorators.http import require_GET

from login.models import User


def session_timeout(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            email = request.session['email']
            user = User.objects.get(email=email)
        except KeyError as e:
            print(e)
            return render(request, 'login/login.html', locals())
        return func(request, *args, **kwargs)
    return wrapper


@session_timeout
@require_GET
def home_page(request):
    user = User.objects.get(email=request.session['email'])
    return render(request, 'home-page.html', locals())

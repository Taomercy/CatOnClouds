from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def home_page(request):
    return render(request, 'home-page.html', locals())

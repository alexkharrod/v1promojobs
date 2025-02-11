from django.shortcuts import render


from core.utils import log_info


def home(request):
    log_info("Home page visited")
    return render(request, "home.html")

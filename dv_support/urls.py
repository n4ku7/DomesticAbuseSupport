from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home_redirect(request):
    return redirect('login')


urlpatterns = [
    path('', home_redirect),
    path('', include('accounts.urls')),
    path('', include('core.urls')),
    path('', include('support.urls')),
    path('admin/', admin.site.urls),
]
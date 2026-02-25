from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db import connection


def home_redirect(request):
    return redirect('login')


def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        db_status = 'ok'
    except Exception:
        db_status = 'error'

    payload = {
        'status': 'ok' if db_status == 'ok' else 'degraded',
        'database': db_status,
    }

    status_code = 200 if db_status == 'ok' else 503
    return JsonResponse(payload, status=status_code)


urlpatterns = [
    path('', home_redirect),
    path('health/', health_check, name='health_check'),
    path('', include('accounts.urls')),
    path('', include('core.urls')),
    path('', include('support.urls')),
    path('', include('communication.urls')),
    path('admin/', admin.site.urls),
]
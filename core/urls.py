from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import path
from .views import dashboard_router

@login_required
def dashboard_router(request):
    user = request.user

    if user.role == 'admin':
        return render(request, 'dashboards/admin_dashboard.html')

    elif user.role == 'survivor':
        return render(request, 'dashboards/survivor_dashboard.html')

    elif user.role == 'counsellor':
        return render(request, 'dashboards/counsellor_dashboard.html')

    elif user.role == 'legal_advisor':
        return render(request, 'dashboards/legal_dashboard.html')

    return redirect('login')

urlpatterns = [
    path('dashboard/', dashboard_router, name='dashboard'),
]
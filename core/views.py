from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from support.models import HelpRequest
from resources.models import Resource


def home_page(request):
    featured_resources = Resource.objects.order_by('-created_at')[:3]
    context = {
        'featured_resources': featured_resources,
    }
    return render(request, 'core/home.html', context)


def services_page(request):
    return render(request, 'core/services.html')


def emergency_page(request):
    emergency_resources = Resource.objects.filter(resource_type='emergency').order_by('-created_at')
    return render(request, 'core/emergency.html', {'emergency_resources': emergency_resources})


@login_required
def dashboard_router(request):
    user = request.user

    if user.is_superuser or user.is_staff:
        context = {
            'total_requests': HelpRequest.objects.count(),
            'pending_requests': HelpRequest.objects.filter(status='pending').count(),
            'assigned_requests': HelpRequest.objects.filter(status='assigned').count(),
            'closed_requests': HelpRequest.objects.filter(status='closed').count(),
        }
        return render(request, 'dashboards/admin_dashboard.html', context)

    if user.role == 'admin':
        context = {
            'total_requests': HelpRequest.objects.count(),
            'pending_requests': HelpRequest.objects.filter(status='pending').count(),
            'assigned_requests': HelpRequest.objects.filter(status='assigned').count(),
            'closed_requests': HelpRequest.objects.filter(status='closed').count(),
        }
        return render(request, 'dashboards/admin_dashboard.html', context)

    elif user.role == 'survivor':
        my_requests = HelpRequest.objects.filter(survivor=user)
        context = {
            'my_total_requests': my_requests.count(),
            'my_pending_requests': my_requests.filter(status='pending').count(),
            'my_assigned_requests': my_requests.filter(status='assigned').count(),
            'my_closed_requests': my_requests.filter(status='closed').count(),
        }
        return render(request, 'dashboards/survivor_dashboard.html', context)

    elif user.role == 'counsellor':
        assigned = HelpRequest.objects.filter(assignment__counsellor=user)
        context = {
            'assigned_total': assigned.count(),
            'assigned_open': assigned.exclude(status='closed').count(),
            'assigned_closed': assigned.filter(status='closed').count(),
        }
        return render(request, 'dashboards/counsellor_dashboard.html', context)

    elif user.role == 'legal_advisor':
        assigned = HelpRequest.objects.filter(assignment__legal_advisor=user)
        context = {
            'assigned_total': assigned.count(),
            'assigned_open': assigned.exclude(status='closed').count(),
            'assigned_closed': assigned.filter(status='closed').count(),
        }
        return render(request, 'dashboards/legal_dashboard.html', context)

    return redirect('login')
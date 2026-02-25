from django.urls import path
from .views import dashboard_router, home_page, services_page, emergency_page

urlpatterns = [
    path('', home_page, name='home'),
    path('services/', services_page, name='services'),
    path('emergency/', emergency_page, name='emergency'),
    path('dashboard/', dashboard_router, name='dashboard'),
]
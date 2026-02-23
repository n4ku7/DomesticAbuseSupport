from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from .forms import SurvivorRegistrationForm


class SurvivorRegisterView(CreateView):
    form_class = SurvivorRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
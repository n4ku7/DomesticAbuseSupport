from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import HelpRequest
from .forms import HelpRequestForm
from accounts.mixins import SurvivorRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from accounts.mixins import SurvivorRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CaseAssignmentForm
from django.views import View


class CreateHelpRequestView(LoginRequiredMixin, SurvivorRequiredMixin, CreateView):
    model = HelpRequest
    form_class = HelpRequestForm
    template_name = 'support/create_request.html'
    success_url = reverse_lazy('dashboard')
    def form_valid(self, form):
        form.instance.survivor = self.request.user
        return super().form_valid(form)

class SurvivorRequestListView(LoginRequiredMixin, SurvivorRequiredMixin, ListView):
    model = HelpRequest
    template_name = 'support/request_list.html'
    context_object_name = 'requests'
    def get_queryset(self):
        return HelpRequest.objects.filter(survivor=self.request.user)
    
class AssignCaseView(LoginRequiredMixin, View):
    template_name = 'support/assign_case.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, pk):
        help_request = get_object_or_404(HelpRequest, pk=pk)
        form = CaseAssignmentForm()
        return render(request, self.template_name, {'form': form, 'help_request': help_request})
    def post(self, request, pk):
        help_request = get_object_or_404(HelpRequest, pk=pk)
        form = CaseAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.help_request = help_request
            assignment.assigned_by = request.user
            assignment.save()
            help_request.status = 'assigned'
            help_request.save()
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form, 'help_request': help_request})
    
class AdminRequestListView(LoginRequiredMixin, ListView):
    model = HelpRequest
    template_name = 'support/request_list.html'
    context_object_name = 'requests'
    def get_queryset(self):
        if self.request.user.role != 'admin':
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return HelpRequest.objects.all()
    
class AssignedCaseListView(LoginRequiredMixin, ListView):
    model = HelpRequest
    template_name = 'support/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        user = self.request.user

        if user.role == 'counsellor':
            return HelpRequest.objects.filter(
                assignment__counsellor=user
            )

        elif user.role == 'legal_advisor':
            return HelpRequest.objects.filter(
                assignment__legal_advisor=user
            )

        else:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
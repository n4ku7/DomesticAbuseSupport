from django.core.exceptions import PermissionDenied


class SurvivorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'survivor':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
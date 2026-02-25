from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SurvivorRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            return None

        user_model = get_user_model()
        existing_user = user_model.objects.filter(email__iexact=email).first()
        if existing_user:
            raise forms.ValidationError(
                'An account with this email already exists. Please log in instead.'
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'survivor'
        user.is_verified = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')
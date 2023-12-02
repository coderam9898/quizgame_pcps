# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Add any additional fields or customization if needed
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

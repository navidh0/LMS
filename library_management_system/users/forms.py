from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=200, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "full_name",)


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)



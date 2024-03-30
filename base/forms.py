from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from base.models import *
User = get_user_model()


class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'email', 'user_title', 'user_bio', 'facebook_link', 'twitter_link',
                  'linkedin_link', 'instagram_link', 'specialty', 'expertise', 'education', 'honors_and_awards',
                  'affiliations']


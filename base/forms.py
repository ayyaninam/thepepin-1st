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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get("email")
    #     password = cleaned_data.get("password")
        
    #     if email and password:
    #         self.user = authenticate(email=email, password=password)
    #         if self.user is None:
    #             raise forms.ValidationError("Invalid email or password.")
    #     return cleaned_data




class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']



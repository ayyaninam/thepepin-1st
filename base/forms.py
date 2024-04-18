from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
from base.models import *


User = get_user_model()


class CustomPasswordValidator:
    def validate(self, password):
        # Check for minimum length
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Check for at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # Check for at least one lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # Check for at least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

    def get_help_text(self):
        return "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character."


class LoginForm(forms.Form):

    email = forms.EmailField(
        label=_("Email"),
        validators=[validate_email],
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    orcid_number = forms.CharField(max_length=2000, required=False)

    class Meta:
        model = User
        fields = ['profile_picture', 'title', 'orcid_number', 'email', 'password1', 'password2', 'research_network_url']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

class UserForm(forms.ModelForm):
    user_bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'style':'height:200px'}))
    user_title = forms.CharField(max_length=100, label='Title', required=False)


    facebook_link = forms.URLField(label='Facebook Link', required=False)
    twitter_link = forms.URLField(label='Twitter Link', required=False)
    linkedin_link = forms.URLField(label='Linkedin Link', required=False)
    instagram_link = forms.URLField(label='Instagram Link', required=False)
    profile_picture = forms.ImageField(label='', required=False)

    
    class Meta:
        model = User
        fields = ['profile_picture', 'user_title', 'user_bio', 'facebook_link', 'twitter_link', 'linkedin_link', 'instagram_link']
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        user_email = kwargs.pop('user_email', None)
        user_title = kwargs.pop('user_title', None)
        user_bio = kwargs.pop('user_bio', None)
        facebook_link = kwargs.pop('facebook_link', None)
        twitter_link = kwargs.pop('twitter_link', None)
        linkedin_link = kwargs.pop('linkedin_link', None)
        instagram_link = kwargs.pop('instagram_link', None)
        profile_picture = kwargs.pop('profile_picture', None)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

        if user_email:
            self.fields['user_email'].initial = user_email

        if user_title:
            self.fields['user_title'].initial = user_title

        if user_bio:
            self.fields['user_bio'].initial = user_bio

        if facebook_link:
            self.fields['facebook_link'].initial = facebook_link
        if twitter_link:
            self.fields['twitter_link'].initial = twitter_link
        if linkedin_link:
            self.fields['linkedin_link'].initial = linkedin_link
        if instagram_link:
            self.fields['instagram_link'].initial = instagram_link

        if profile_picture:
            self.fields['profile_picture'].initial = profile_picture

class EventForm(forms.ModelForm):



    class Meta:
        model = Event
        fields = ['cover_image', 'owner_or_institution_name', 'title', 'short_description',  'description', 'date', 'location', 'link_to_orignal']

        widgets = {
            'description': forms.Textarea(attrs={
                "rows":5,
                'style': 'height: 250px;'
                
                }),
            'short_description': forms.Textarea(attrs={
                "rows":5,
                'style': 'height: 150px;'
                
                }),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['cover_image'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    


class SearcherForm(forms.ModelForm):

    class Meta:
        model = Searcher
        fields = ['title', 'name_of_researcher', 'thumbnail', 'video_url']
        labels = {
            'title': 'Title',
            'name_of_researcher': 'Name of Researcher',
            'video_url': 'Video URL',
            'thumbnail': 'Thumbnail',
        }
        
    def __init__(self, *args, **kwargs):
        super(SearcherForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

class ForgetPassswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ForgetPassswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
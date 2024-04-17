from django.contrib.auth.models import AbstractUser
from base.manager import UserManager
from django.db import models
import os
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USERNAME_FIELD = 'email'

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/default_pp.png')
    email = models.EmailField(unique=True)
    title = models.ForeignKey('title', null=True, blank=True, on_delete=models.CASCADE)
    user_bio = models.TextField(blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    facebook_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    profile_views = models.PositiveIntegerField(default=0)
    total_publications = models.PositiveIntegerField(default=0)
    publication_views = models.PositiveIntegerField(default=0)
    publication_downloads = models.PositiveIntegerField(default=0)
    specialty = models.ManyToManyField('Specialty', related_name='users', blank=True)
    expertise = models.ManyToManyField('Expertise', related_name='users', blank=True)
    education = models.ManyToManyField('Education', related_name='users', blank=True)
    honors_and_awards = models.ManyToManyField('HonorsAndAwards', related_name='users', blank=True)
    affiliations = models.ManyToManyField('Affiliation', related_name='users', blank=True)


    orcid_number = models.TextField(null=True, blank=True)
    research_network_url = models.URLField(null=True, blank=True)


    objects = UserManager()


    username = None
    REQUIRED_FIELDS = []  # Add any additional required fields here

    def __str__(self) -> str:
        return self.email
    

class Title(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self) -> str:
        return self.name

class Specialty(models.Model):
    # user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='SpecialtyUser', blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

class Expertise(models.Model):
    # user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='ExpertiseUser', blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

class Education(models.Model):
    # user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='EducationUser', blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

class HonorsAndAwards(models.Model):
    # user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='HonorsAndAwardsUser', blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

class Affiliation(models.Model):
    # user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='AffiliationUser', blank=False)

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    institution_name = models.ForeignKey('Institution', related_name='affiliation', blank=True, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    CURRENT = 'Current'
    PAST = 'Past'
    STATE_CHOICES = [
        (CURRENT, 'Current'),
        (PAST, 'Past'),
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, blank=True, null=True)


    def __str__(self) -> str:
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='articleUser', blank=False)
    article_type = models.ForeignKey('ArticleType', on_delete=models.CASCADE, related_name='articlestype', blank=True)
    resources = models.ManyToManyField('Resources', related_name='articles', blank=True)
    description = models.TextField()
    disclaimer = models.TextField(blank=True)
    copyright = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_articles', blank=True, null=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edited_articles', blank=True, null=True)
    received_date = models.DateField(blank=True, null=True, auto_now_add=True)
    accepted_date = models.DateField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True, auto_now_add=True)
    keywords = models.ManyToManyField('Keyword', related_name='articles', blank=True)
    institution = models.ForeignKey('Institution', related_name='institution_articles', on_delete=models.CASCADE, blank=True)
    views=  models.PositiveIntegerField(null=False, blank=False, default=0)


    def __str__(self) -> str:
        return self.title[:100]

class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class ArticleType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class Resources(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='article_resources/', blank=True, null=True, help_text='Accepted file formats: Latex, doc, docx, odt, png, jpeg, gif, ps, eps, tif, tiff, pdf')

    def get__name(self):
        if self.name:
            return self.name
        elif self.file:
            return os.path.basename(self.file.name)
        else:
            return "NO NAME"

class Institution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    owner_or_institution_name = models.CharField(_("owner_or_institution_name"), max_length=250, null=False, blank=False, default='admin')
    title = models.CharField(_("title"), max_length=250, null=False, blank=False)
    short_description = models.TextField(_("short_description"), null=False, blank=False)
    cover_image = models.ImageField(_("cover_image"), upload_to="base/culture_cover/", null=True, blank=True)
    description = models.TextField(_("description"), null=False, blank=False)
    date = models.DateField(_("date"), null=False, blank=False)
    location = models.CharField(_("location"), max_length=255, null=True, blank=True)
    link_to_orignal = models.URLField(_("link_to_orignal"), max_length=1000)


class Searcher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    name_of_researcher = models.CharField(max_length=255, null=False, blank=False)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    video_url = models.URLField(null=False, blank=False, default="https://www.youtube.com/", help_text="Please Upload your Video on Youtube and Paste Link here...")
    thumbnail = models.ImageField(upload_to="searcher_thumb", null=False, blank=False)


    def __str__(self) -> str:
        return self.title
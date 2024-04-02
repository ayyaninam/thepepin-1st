from django.contrib.auth.models import AbstractUser
from base.manager import UserManager
from django.db import models
import os

class User(AbstractUser):
    USERNAME_FIELD = 'email'

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/default_pp.png')
    email = models.EmailField(unique=True)
    user_title = models.CharField(max_length=100, blank=True)
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


    objects = UserManager()


    username = None
    REQUIRED_FIELDS = []  # Add any additional required fields here

    def __str__(self) -> str:
        return self.email
    

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
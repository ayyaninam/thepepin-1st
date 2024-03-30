from django.urls import path, include
from base import views
urlpatterns = [
    path('', views.homepage_view, name="homepage_view"),
    path('article/<int:id>', views.article_view, name="article_view"),
    path('login', views.login_view, name="login_view"),
    path('signup', views.signup_view, name="signup_view"),
    path('logout', views.logout_view, name='logout_view'),
    path('create-article', views.create_article_view, name='create_article_view'),
    path('user-profile-edit-view', views.user_profile_edit_view, name='user_profile_edit_view'),
]
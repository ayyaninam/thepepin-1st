from django.urls import path, include
from base import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.homepage_view, name="homepage_view"),
    path('article/<int:id>', views.article_view, name="article_view"),
    path('login', views.login_view, name="login_view"),
    path('signup', views.signup_view, name="signup_view"),
    path('logout', views.logout_view, name='logout_view'),
    # path('forget-password', views.forget_password_view, name='forget_password_view'),
    path('create-article', views.create_article_view, name='create_article_view'),
    path('user-profile-edit-view', views.user_profile_edit_view, name='user_profile_edit_view'),
    path('searcher', views.searcher, name='searcher'),
    path('create-event', views.create_event, name='create_event'),
    path('create-searcher', views.create_searcher, name='create_searcher'),
    path('events', views.events, name='events'),
    path('event-post/<int:post_id>', views.event_post, name='event_post'),
    path('profile-view/<int:id>', views.profile_view, name='profile_view'),



    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='base/password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset/reset.html'), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='base/password_reset/password_reset.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
]
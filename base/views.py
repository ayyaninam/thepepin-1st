from django.shortcuts import render, redirect, get_object_or_404
from base.forms import LoginForm, SignupForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate

from django.contrib import messages
from django.http import Http404
from base.models import * 
from django.urls import reverse


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login_view'))  # Redirect to your login page
        return view_func(request, *args, **kwargs)
    return wrapper

def homepage_view(request):

    all_articles = None

    sort = request.GET.get('sort') if request.GET.get('sort') != None else 'recent'

    if sort=='recent':
        all_articles = Article.objects.all().order_by('-published_date')
    
    elif sort=='viewed':
        all_articles = Article.objects.all().order_by('-views')
        
    context = {
        'all_articles':all_articles,
    }
    return render(request, 'base/homepage.html', context)




def article_view(request, id):

    try:
        article = get_object_or_404(Article, id=id)
        latest_articles = Article.objects.all().order_by('-published_date')
    except Http404:
        # Handle the 404 error here, such as rendering a custom 404 page
        return render(request, '404.html')
    
    context = {
        'article': article,
        'latest_articles': latest_articles,
    }

    return render(request, 'base/article.html', context=context)


def login_view(request):
    if request.method == 'POST':
        userobj = User.objects.filter(email=request.POST['email'])
        if userobj:
            userobj = userobj.first()
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login_view')
        
        form = LoginForm(request.POST, request.FILES, instance=userobj)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('homepage_view')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'base/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('homepage_view')
        
        else:
            return render(request, 'base/signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'base/signup.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('homepage_view')


@login_required
def create_article_view(request):
    return render(request, 'base/create_article.html')

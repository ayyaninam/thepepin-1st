from django.shortcuts import render, redirect, get_object_or_404
from base.forms import LoginForm, SignupForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate

from django.contrib import messages
from django.http import Http404
from base.models import * 
from django.urls import reverse
from base.forms import *


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
    context = {}
    if request.method == 'POST':
        # Process form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        article_type = request.POST.get('article_type')
        disclaimer = request.POST.get('disclaimer')
        copyright = request.POST.get('copyright')
        institution = request.POST.get('institute')

        user = request.user
        if not user:
            error_message = f"User not logged in properly"
            messages.error(request, error_message)
            return redirect('homepage_view') 
        if not title:
            error_message = f"Please add title!"
            messages.error(request, error_message)
            return redirect('homepage_view') 
        if not description:
            error_message = f"Please add description!"
            messages.error(request, error_message)
            return redirect('homepage_view') 
        if not institution:
            error_message = f"Please add institution!"
            messages.error(request, error_message)
            return redirect('homepage_view') 
        
        if not article_type:
            error_message = f"Please add article_type!"
            messages.error(request, error_message)
            return redirect('homepage_view') 
        

        # Process Article Type
        try:
            art_type_obj, created = ArticleType.objects.get_or_create(name = article_type)
        except Exception as e:
            error_message = f"Error occurred while processing. Error message: {str(e)}"
            messages.error(request, error_message)
            return redirect('homepage_view')

        try:
            institution_obj, created = Institution.objects.get_or_create(name = institution)
        except Exception as e:
            error_message = f"Error occurred while processing. Error message: {str(e)}"
            messages.error(request, error_message)
            return redirect('homepage_view')
            

        # Process keywords
        created_keyword_ids = []
        keywords = request.POST.get('all_keywords')
        keywords = keywords.split(',') if keywords else None
        for keyword in keywords:
            try:
                keyword_obj, created = Keyword.objects.get_or_create(name=keyword)
                created_keyword_ids.append(keyword_obj.id)
            except Exception as e:
                error_message = f"Error occurred while processing. Error message: {str(e)}"
                messages.error(request, error_message)
                return redirect('homepage_view') 
        # End Process keywords

        # Process resources
        created_resource_ids = []

        for file in request.FILES:
            try:
                if 'file' in file:
                    saveable_file = request.FILES.get(f'{file}')
                    filename = ((request.POST.get(f'filename{file.split("file")[1]}')) or (saveable_file.name))

                    created_res = Resources.objects.create(
                        name = filename,
                        file = saveable_file,
                    )

                    created_resource_ids.append(created_res.id)

            except Exception as e:
                error_message = f"Error occurred while processing file: {file}. Error message: {str(e)}"
                messages.error(request, error_message)
                return redirect('homepage_view') 
            

        
        created_article = Article.objects.create(
            title = title,
            description = description,
            user = user,
            institution=institution_obj,
            article_type=art_type_obj,
            # resources=created_resource_ids,
            # keywords=created_keyword_ids,
            disclaimer = disclaimer,
            copyright = copyright,
        )
        created_article.resources.add(*created_resource_ids)
        created_article.keywords.add(*created_keyword_ids)
        created_article.save()
    
    
    else:
        articletypes = ArticleType.objects.all()
        institution = Institution.objects.all()
        context.update({'articletypes':articletypes})
        context.update({'institutions': institution})

    return render(request, 'base/create_article.html', context)


@login_required
def user_profile_edit_view(request):
    if request.method == 'POST':

        specialties = {}
        education = {}
        awards_honour = {}
        expertise = {}
        affiliation = {}

        # request.user.specialty.create(title="Fake", description="Fake", user=request.user)
        for key, value in request.POST.items():
            if key == "first_name":
                request.user.update(first_name = value) if request.user.first_name != value else None
            elif key == "last_name":
                request.user.update(last_name = value) if request.user.last_name != value else None
            elif key == "user_title":
                request.user.update(user_title = value) if request.user.user_title != value else None
            elif key == "user_bio":
                request.user.update(user_bio = value) if request.user.user_bio != value else None
            elif key == "facebook_link":
                request.user.update(facebook_link = value) if request.user.facebook_link != value else None
            elif key == "twitter_link":
                request.user.update(twitter_link = value) if request.user.twitter_link != value else None
            elif key == "linkedin_link":
                request.user.update(linkedin_link = value) if request.user.linkedin_link != value else None
            elif key == "instagram_link":
                request.user.update(instagram_link = value) if request.user.instagram_link != value else None

            elif ((key.startswith("specialty")) and not ('desc_' in key)):
                specialties.update({value:None})

            elif ((key.startswith("specialtydesc_"))):
                specialties.update({f"specialty{key.split('desc_')[1]}":value})

            elif ((key.startswith("education")) and not ('desc_' in key)):
                education.update({value:None})

            elif ((key.startswith("educationdesc_"))):
                education.update({f"education{key.split('desc_')[1]}":value})

            elif ((key.startswith("expertise")) and not ('desc_' in key)):
                expertise.update({value:None})

            elif ((key.startswith("expertisedesc_"))):
                expertise.update({f"expertise{key.split('desc_')[1]}":value})

            elif ((key.startswith("affiliation")) and not ('desc_' in key)):
                affiliation.update({value:None})

            elif ((key.startswith("affiliationdesc_"))):
                affiliation.update({f"affiliation{key.split('desc_')[1]}":value})

            elif ((key.startswith("honourandawards")) and not ('desc_' in key)):
                awards_honour.update({value:None})

            elif ((key.startswith("honourandawardsdesc_"))):
                awards_honour.update({f"honourandawards{key.split('desc_')[1]}":value})

            for key, value in specialties.items():
                request.user.specialty.create(title=key, description=value)
            for key, value in education.items():
                request.user.education.create(title=key, description=value)
            for key, value in awards_honour.items():
                request.user.honors_and_awards.create(title=key, description=value)
            for key, value in expertise.items():
                request.user.expertise.create(title=key, description=value)
            for key, value in affiliation.items():
                request.user.affiliations.create(title=key, description=value)

# <QueryDict: {'csrfmiddlewaretoken': ['sQTKnO5upgz9BfWDT3NuoCALqQN67y6J2qQeW2Ctk1ONwV6Ogz4B4yYV3bdtHJs9'], 'first_name': ['Ayyan'], 'last_name': ['Inam'], 'user_title': ['Hello World'], 'user_bio': ['HWELLO iaeydsj\r\nEHlasd'], 'facebook_link': ['https://www.facebook.com/'], 'twitter_link': ['https://www.facebook.com/'], 'linkedin_link': ['https://www.facebook.com/'], 'instagram_link': ['https://www.facebook.com/'], 'specialty_1': ['Hello'], 'specialty_desc_1': ['Yes'], 'specialty2': ['sdf'], 'specialty_desc_2': ['sdfsd'], 'specialty3': ['sdf'], 'specialty_desc_3': ['sdf'], 'expertise1': ['sdfs'], 'expertise_desc_1': ['sdf'], 'expertise2': ['sdf'], 'expertise_desc_2': ['sdf'], 'education1': ['sdf'], 'education_desc_1': ['sdf'], 'education2': ['sdf'], 'education_desc_2': ['sdf'], 'affiliation1': ['sdf'], 'affiliation_desc_1': ['sdf'], 'affiliation2': ['sdf'], 'affiliation_desc_2': ['sdf'], 'honourandawards1': ['sdf'], 'honourandawards_desc_1': ['sdf']}>

    return render(request, 'base/user_profile_edit.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.forms import LoginForm, SignupForm
from django.contrib.auth import login as dj_login


from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from base.models import * 
from base.forms import *
from django.conf import settings




def login_view(request):
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(email=email, password=password)

            if user is not None:
                dj_login(request, user)

                redirect_url = request.POST.get('redirect_url') if request.POST.get('redirect_url') else settings.LOGOUT_REDIRECT_URL

                return redirect(redirect_url)
            else:
                form.add_error('password', "No! Account Found. Please enter a correct email and password. Note that both fields may be case-sensitive")
                return render(request, 'base/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'base/login.html', {'form': form})



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            dj_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('homepage_view')
        
        else:
            return render(request, 'base/signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'base/signup.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('homepage_view')


def forget_password_view(request):
    if request.method == "POST":
        print(request.POST)
        form = ForgetPassswordForm(None, request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form  = ForgetPassswordForm()
    return render(request, 'base/forget_passsword.html', {'form': form})



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
        article.views = article.views + 1
        if not article.user == request.user:
            article.user.publication_views = article.user.publication_views + 1
        article.save()
        latest_articles = Article.objects.all().order_by('-published_date')
    except Http404:
        # Handle the 404 error here, such as rendering a custom 404 page
        return render(request, '404.html')
    
    context = {
        'article': article,
        'latest_articles': latest_articles,
    }

    return render(request, 'base/article.html', context=context)



def profile_view(request, id):
    try:
        user = User.objects.get(id=id)
        all_articles = Article.objects.filter(user=user).order_by('-published_date')
        print(all_articles)
        if not user == request.user:
            user.profile_views = user.profile_views + 1
        user.save()

    except:
        messages.error(request, "No Profile Found")
        return render(request, 'base/profile_view.html')
    
    context = {
        'user':user,
        "all_articles":all_articles,
    }
    return render(request, 'base/profile_view.html', context)

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
        request.user.total_publications = request.user.total_publications+1
        request.user.save()
    
    
    else:
        articletypes = ArticleType.objects.all()
        institution = Institution.objects.all()
        context.update({'articletypes':articletypes})
        context.update({'institutions': institution})

    return render(request, 'base/create_article.html', context)


@login_required
def user_profile_edit_view(request):
    if request.method == 'POST':
        user = request.user
        # print(request.POST)
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None)
        user_title = request.POST.get('user_title',None)
        user_bio = request.POST.get('user_bio',None)
        facebook_link = request.POST.get('facebook_link',None)
        twitter_link = request.POST.get('twitter_link',None)
        linkedin_link = request.POST.get('linkedin_link',None)
        instagram_link = request.POST.get('instagram_link',None)

        user.first_name = first_name
        user.last_name = last_name
        user.user_title = user_title
        user.user_bio = user_bio
        user.facebook_link = facebook_link
        user.twitter_link = twitter_link
        user.linkedin_link = linkedin_link
        user.instagram_link = instagram_link








        filtered_keys = set()
        prefixes = ['specialty', 'education', 'expertise', 'affiliation', 'honourandawards']

        for key in request.POST.keys():
            if any(key.startswith(prefix) for prefix in prefixes):
                if "desc_" in key:
                    original_key = key.replace('desc_', '', 1)
                    if original_key in filtered_keys:
                        filtered_keys.discard(original_key)
                filtered_keys.add(key)

        filtered_keys_list = list(filtered_keys)


        user.specialty.all().delete()
        user.education.all().delete()
        user.expertise.all().delete()
        user.affiliations.all().delete()
        user.honors_and_awards.all().delete()

        for value in filtered_keys_list:
            key = int(''.join(filter(str.isdigit, value)))

            if (value.startswith('specialty')):
                user.specialty.create(
                    title=request.POST.get(f'specialty{key}', None),
                    description=request.POST.get(f'specialtydesc_{key}', None)
                    )
            elif (value.startswith('education')):
                user.education.create(
                    title=request.POST.get(f'education{key}', None),
                    description=request.POST.get(f'educationdesc_{key}', None)
                    )
            elif (value.startswith('expertise')):
                user.expertise.create(
                    title=request.POST.get(f'expertise{key}', None),
                    description=request.POST.get(f'expertisedesc_{key}', None)
                    )
            elif (value.startswith('affiliation')):
                user.affiliations.create(
                    title=request.POST.get(f'affiliation{key}', None),
                    description=request.POST.get(f'affiliationdesc_{key}', None)
                    )
            elif (value.startswith('honourandawards')):
                user.honors_and_awards.create(
                    title=request.POST.get(f'honourandawards{key}', None),
                    description=request.POST.get(f'honourandawardsdesc_{key}', None)
                    )

        profile_picture = request.FILES.get('profilePictureInput', None)

        if profile_picture:
            user.profile_picture=profile_picture

        user.save()

        return HttpResponseRedirect(request.path_info)


    return render(request, 'base/user_profile_edit.html')
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

# core/views.py
from item.models import Category, Item
from .forms import SignupForm, ProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
# Create your views here.

def index(request):
    item_list = Item.objects.filter(is_sold=False).order_by('-created_at')
    paginator = Paginator(item_list, 6) # Show 6 items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'core/index.html', {
        'items': page_obj,
        'categories': categories,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account created successfully! Welcome to the marketplace.')
            return redirect('core:setup_profile')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form,
    })

@login_required
def setup_profile(request):
    profile = getattr(request.user, 'profile', None)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            
            # Handle cropped image
            cropped_image = request.POST.get('cropped_image')
            if cropped_image:
                try:
                    format, imgstr = cropped_image.split(';base64,')
                    ext = format.split('/')[-1]
                    data = ContentFile(base64.b64decode(imgstr), name=f'{request.user.username}_profile.{ext}')
                    profile.image = data
                    profile.save()
                except Exception as e:
                    print(f"Error processing cropped image: {e}")
            
            return redirect('/')
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'core/setup_profile.html', {
        'form': form
    })

@login_required
def settings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = p_form.save()
            
            # Handle cropped image
            cropped_image = request.POST.get('cropped_image')
            if cropped_image:
                try:
                    format, imgstr = cropped_image.split(';base64,')
                    ext = format.split('/')[-1]
                    data = ContentFile(base64.b64decode(imgstr), name=f'{request.user.username}_profile.{ext}')
                    profile.image = data
                    profile.save()
                except Exception as e:
                    print(f"Error processing cropped image: {e}")
                    
            messages.success(request, 'Your account has been updated!')
            return redirect('core:settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    return render(request, 'core/settings.html', {
        'u_form': u_form,
        'p_form': p_form
    })

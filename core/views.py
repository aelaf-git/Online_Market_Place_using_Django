from django.shortcuts import render, redirect

# core/views.py
from item.models import Category, Item
from .forms import SignupForm, ProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    items = Item.objects.filter(is_sold=False).order_by('-created_at')[:10]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'items': items,
        'categories': categories,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
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
            form.save()
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
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('core:settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    return render(request, 'core/settings.html', {
        'u_form': u_form,
        'p_form': p_form
    })

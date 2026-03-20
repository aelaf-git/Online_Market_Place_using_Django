from django.shortcuts import render, redirect

# core/views.py
from item.models import Category, Item
from .forms import SignupForm, ProfileForm
from django.contrib.auth.decorators import login_required
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

from django.shortcuts import render

# core/views.py
from item.models import Category, Item
from .forms import SignupForm
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
    form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form,
    })

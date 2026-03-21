from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'bio', 'phone_number')
    
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-5 py-3 bg-black border border-zinc-800 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] transition-colors duration-200',
    }))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Tell us about yourself...',
        'rows': 3,
        'class': 'w-full px-5 py-3 bg-black border border-zinc-800 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] transition-colors duration-200',
    }))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'w-full px-5 py-3 bg-black border border-zinc-800 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] transition-colors duration-200',
    }))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'w-full px-5 py-4 bg-black border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] focus:ring-1 focus:ring-[#1D9BF0] transition-all duration-200',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'w-full px-5 py-4 bg-black border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] focus:ring-1 focus:ring-[#1D9BF0] transition-all duration-200',
    }))

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'w-full px-5 py-4 bg-black border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] focus:ring-1 focus:ring-[#1D9BF0] transition-all duration-200',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'w-full px-5 py-4 bg-black border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] focus:ring-1 focus:ring-[#1D9BF0] transition-all duration-200',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'w-full px-5 py-4 bg-black border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] focus:ring-1 focus:ring-[#1D9BF0] transition-all duration-200',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'w-full px-5 py-4 bg-black border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#1D9BF0] focus:ring-1 focus:ring-[#1D9BF0] transition-all duration-200',
    }))
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
    
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'w-full px-5 py-3 bg-slate-800/50 border border-cyan-600/50 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 focus:shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-all duration-300',
    }))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'w-full px-5 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 focus:shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-all duration-300',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'password',
        'class': 'w-full px-5 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 focus:shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-all duration-300',
    }))

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'w-full px-5 py-3 bg-slate-800/50 border border-purple-600/50 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 focus:shadow-[0_0_15px_rgba(168,85,247,0.3)] transition-all duration-300',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'w-full px-5 py-3 bg-slate-800/50 border border-purple-600/50 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 focus:shadow-[0_0_15px_rgba(168,85,247,0.3)] transition-all duration-300',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'password',
        'class': 'w-full px-5 py-3 bg-slate-800/50 border border-purple-600/50 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 focus:shadow-[0_0_15px_rgba(168,85,247,0.3)] transition-all duration-300',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
        'class': 'w-full px-5 py-3 bg-slate-800/50 border border-purple-600/50 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 focus:shadow-[0_0_15px_rgba(168,85,247,0.3)] transition-all duration-300',
    }))
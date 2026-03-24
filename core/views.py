from django.shortcuts import render, redirect

# core/views.py
from item.models import Category, Item
from .forms import SignupForm, ProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import EmailVerification
from django.core.mail import send_mail
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
            user = form.save(commit=False)
            user.is_active = False # Deactivate user until verified
            user.save()
            
            # Generate and send verification code
            code = EmailVerification.generate_code(user)
            send_mail(
                'Verify your email',
                f'Your verification code is: {code}. It expires in 5 minutes.',
                'noreply@online-marketplace.com',
                [user.email],
                fail_silently=False,
            )
            
            # Store user ID in session for verification process
            request.session['verification_user_id'] = user.id
            messages.info(request, 'An 8-digit verification code has been sent to your email.')
            return redirect('core:verify_email')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form,
    })

def verify_email(request):
    user_id = request.session.get('verification_user_id')
    if not user_id:
        return redirect('core:signup')
    
    try:
        user = User.objects.get(id=user_id)
        verification = user.email_verification
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        return redirect('core:signup')

    if request.method == 'POST':
        code = request.POST.get('code')
        if code == verification.code:
            if not verification.is_expired():
                user.is_active = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['verification_user_id']
                messages.success(request, 'Email verified successfully! Welcome to the marketplace.')
                return redirect('core:index')
            else:
                messages.error(request, 'Verification code has expired. Please request a new one.')
        else:
            messages.error(request, 'Invalid verification code.')

    return render(request, 'core/verify_email.html', {'email': user.email})

def resend_verification_code(request):
    user_id = request.session.get('verification_user_id')
    if not user_id:
        return redirect('core:signup')
    
    try:
        user = User.objects.get(id=user_id)
        code = EmailVerification.generate_code(user)
        send_mail(
            'Verify your email',
            f'Your new verification code is: {code}. It expires in 5 minutes.',
            'noreply@online-marketplace.com',
            [user.email],
            fail_silently=False,
        )
        messages.info(request, 'A new verification code has been sent to your email.')
    except User.DoesNotExist:
        return redirect('core:signup')
        
    return redirect('core:verify_email')

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

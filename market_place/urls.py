from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('core.urls')),
    path('items/', include(('item.urls', 'item'), namespace='item')),
    path('admin/', admin.site.urls),
    path('conversations/', include(('conversation.urls', 'conversation'), namespace='conversation')),
    path('cart/', include('cart.urls')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('accounts/', include('allauth.urls')),
    path('chatbot/', include('chatbot.urls')),
] # No static(settings.MEDIA_URL, ...) because we use Cloudinary

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # ← This line was missing!
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),  # Includes chatbot, register, login, logout

    # Custom login and logout using your beautiful templates
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

# Serve media files during development (for future image upload)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
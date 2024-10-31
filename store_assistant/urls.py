from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('voice_recognition.urls')),  # Includes URLs from the voice_recognition app
]

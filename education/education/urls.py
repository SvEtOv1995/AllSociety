from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),
    path("character/", include("character.urls")),
    path('schedule/', include('schedule.urls')),
    path('calculator/', include('calculator.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

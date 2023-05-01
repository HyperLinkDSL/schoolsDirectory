from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import Home, About

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('accounts.urls', namespace="profiles")),
    path('schools/', include('schools.urls', namespace="schools")),
    path('about', About.as_view(), name="about"),
    path('', Home.as_view(), name="home")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

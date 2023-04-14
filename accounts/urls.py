"""
URL configuration for openPublisher project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from accounts import views as profile_views

app_name = "profiles"

urlpatterns = [
    path('create', profile_views.CreateProfile.as_view(), name="create"),
    path('list', profile_views.ListProfiles.as_view(), name="list"),
    path('<pk>/delete', profile_views.DeleteProfile.as_view(), name="delete"),
    path('<pk>/update', profile_views.UpdateProfile.as_view(), name="update"),
    path('login', profile_views.Login.as_view(), name="login"),
    path('logout', profile_views.Logout.as_view(), name="logout"),
]


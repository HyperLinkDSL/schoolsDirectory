
from django.urls import path

from schools import views

app_name = "schools"

urlpatterns = [
    path('create', views.CreateSchool.as_view(), name="create"),
    path('list', views.ListSchools.as_view(), name="list"),
    path('<pk>/delete', views.DeleteSchool.as_view(), name="delete"),
    path('<pk>/update', views.UpdateSchool.as_view(), name="update"),
]


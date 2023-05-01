
from django.urls import path

from schools import views

app_name = "schools"

urlpatterns = [
    path('create', views.CreateSchool.as_view(), name="create"),
    path('list', views.ListSchools.as_view(), name="list"),
    path('<pk>/delete', views.DeleteSchool.as_view(), name="delete"),
    path('<pk>/update', views.UpdateSchool.as_view(), name="update"),
    path('<pk>/upload-pictures', views.UploadPictures.as_view(), name="upload_pictures"),
    path('<pk>/approve', views.ApproveSchool.as_view(), name="approve"),
    path('<pk>/details', views.SchoolDetails.as_view(), name="details"),
]


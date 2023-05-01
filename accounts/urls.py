from django.urls import path
from accounts import views

app_name = "profiles"

urlpatterns = [
    path('create', views.CreateProfile.as_view(), name="create"),
    path('list', views.ListProfiles.as_view(), name="list"),
    path('<pk>/delete', views.DeleteProfile.as_view(), name="delete"),
    path('<pk>/update', views.UpdateProfile.as_view(), name="update"),
    path('signup', views.SignUp.as_view(), name="signup"),
    path('activate/<uidb64>/<token>', views.ActivateAccount.as_view(), name="activate"),
    path('request-password-change', views.RequestPasswordChange.as_view(), name="request_password_change"),
    path('reset-requested-password', views.ChangeRequestedPassword.as_view(), name="reset_requested_password"),
    path('login', views.Login.as_view(), name="login"),
    path('logout', views.Logout.as_view(), name="logout"),
]

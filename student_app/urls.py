from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.home),
    path('register', views.RegisterView.as_view(), name="register"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('login', views.LoginView.as_view(), name="login"),
    # path('writing-tests', views.WritingTestsView.as_view(), name="writing_tests"),
    path('logout', views.Logout.as_view(), name="logout"),
    
] 
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.home),
    path('register', views.TeacherRegisterView.as_view(), name="register"),
    path('profile', views.TeacherProfileView.as_view(), name="profile"),
    path('login', views.TeacherLoginView.as_view(), name="login"),
    path('writing-tests', views.WritingTestsView.as_view(), name="writing_tests"),
    path('listning-tests', views.ListeningTestsView.as_view(), name="listning_tests"),
    path('speaking-tests', views.SpeakingTestsView.as_view(), name="speaking_tests"),
    path('logout', views.TeacherLogout.as_view(), name="logout"),
    
] 
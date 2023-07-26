from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register', views.TeacherRegisterView.as_view(), name="register"),
    path('profile', views.TeacherProfileView.as_view(), name="profile"),
    path('login', views.TeacherLoginView.as_view(), name="login"),
    path('writingTests', views.WritingTestsView.as_view(), name="writing_tests"),
    path('listningTests', views.ListeningTestsView.as_view(), name="listning_tests"),
    path('speakingTests', views.SpeakingTestsView.as_view(), name="speaking_tests"),
    path('readingTests', views.ReadingTestsView.as_view(), name="reading_tests"),
    path('logout', views.TeacherLogout.as_view(), name="logout"),
    path('Check Writing TestView', views.CheckWritingTestView.as_view(), name="CheckWritingTestView"),
    path('Questions List View', views.QuestionsListView.as_view(), name="QuestionsListView"),
    
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
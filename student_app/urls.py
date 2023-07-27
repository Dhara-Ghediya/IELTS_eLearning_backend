from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
urlpatterns = [
    # path('', views.home),
    path('', include('rest_framework.urls')),
    path('register', views.RegisterView.as_view(), name="register"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('login', views.LoginView.as_view(), name="login"),
    # path('writing-tests', views.WritingTestsView.as_view(), name="writing_tests"),
    path('logout', views.Logout.as_view(), name="logout"),
    path('writing test', views.WritingTestView.as_view(), name="writingTestView"),
    path('reading test', views.ReadingTestView.as_view(), name="readingTestView"),
    path('listing test', views.ListingTestView.as_view(), name="listingTestView"),
    path('speaking test', views.SpeakingTestView.as_view(), name="speakingTestView"),
    
    path('student-myTests-writingTest', views.StudentWritingTestAnswersLists.as_view(), name="StudentWritingTestAnswersLists"),
    
] 

# router = DefaultRouter()
# router.register('listing test', views.ListingTestView, basename='listingTestView')
# urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
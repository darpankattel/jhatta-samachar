from django.urls import path
from .views import GoogleAuthView, UserLogoutView, UserProfileView, PreferenceView
from .views import HardcodedLoginView

urlpatterns = [
    path('google/', GoogleAuthView.as_view(), name='google-auth'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('preferences/', PreferenceView.as_view(), name='preferences'),

    path('hardcoded-login/', HardcodedLoginView.as_view(),
         name='hardcoded-login'),
]

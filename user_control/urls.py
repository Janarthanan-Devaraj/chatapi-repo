from django.urls import path, include
from .views import (LoginView, RegisterView, 
                    UserProfileView, MeView, 
                    ProfileView, UpdateFavoriteView, CheckIsFavoriteView)
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter(trailing_slash=False)

router.register("profile", UserProfileView)

urlpatterns = [
    path('', include(router.urls)),
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('me', MeView.as_view()),
    path('myprofile', ProfileView.as_view()),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('update-favorite', UpdateFavoriteView.as_view()),
    path('check-favorite/<int:favorite_id>', CheckIsFavoriteView.as_view())
]
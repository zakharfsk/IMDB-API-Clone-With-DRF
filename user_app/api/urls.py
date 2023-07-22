from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user_app.api.views import registration_view, logout_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='login'),
    path('register/', registration_view, name='register'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='logout'),
]

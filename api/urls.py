from django.urls import path, include
import api.checklist.routes

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import ExtraTokenObtainPairView, get_user_data

app_name = 'api'
urlpatterns = [
	path('checklist/', include(api.checklist.routes)),
    # JWT AUTHENTICATION
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/extras/', ExtraTokenObtainPairView.as_view(), name="token-extras"), # /token + extra user data
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', get_user_data, name='user'),
]
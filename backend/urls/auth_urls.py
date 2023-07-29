from django.urls import path, include

from backend.controllers.auth_views import UserRegisterViewSet, SemdCustomTokenObtainPairView, \
    SemdCustomTokenRefreshView
from backend.routers.auth_routers import UserRouter

user_router = UserRouter()
user_router.register(r'', UserRegisterViewSet)

urlpatterns = [
    path('api/user/', include(user_router.urls)),
    path("api/user/login", SemdCustomTokenObtainPairView.as_view(), name="token"),
    path("api/user/refresh_token", SemdCustomTokenRefreshView.as_view(), name="refresh_token"),
]

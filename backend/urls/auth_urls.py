from django.urls import path, include

from backend.views.auth_views import UserRegisterViewSet, SemdCustomTokenObtainPairView, \
    SemdCustomTokenRefreshView
from backend.routers.auth_routers import UserRouter
from semd.settings import API_PREFIX

user_router = UserRouter()
user_router.register(r'', UserRegisterViewSet)

urlpatterns = [
    path(API_PREFIX + 'user/', include(user_router.urls)),
    path(API_PREFIX + 'user/login', SemdCustomTokenObtainPairView.as_view(), name='token'),
    path(API_PREFIX + 'user/refresh_token', SemdCustomTokenRefreshView.as_view(), name='refresh_token'),
]

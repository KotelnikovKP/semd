from django.urls import path, include

from backend.routers import UserRouter, MedicalServiceRouter, DiagnosisRouter, MedicalOrganizationRouter
from backend.views import UserRegisterViewSet, SemdCustomTokenObtainPairView, SemdCustomTokenRefreshView, \
    MedicalServiceViewSet, DiagnosisViewSet, MedicalOrganizationViewSet

medical_service_router = MedicalServiceRouter()
medical_service_router.register(r'medical_service', MedicalServiceViewSet)
diagnosis_router = DiagnosisRouter()
diagnosis_router.register(r'diagnosis', DiagnosisViewSet)
medical_organization_router = MedicalOrganizationRouter()
medical_organization_router.register(r'medical_organization', MedicalOrganizationViewSet)
user_router = UserRouter()
user_router.register(r'user', UserRegisterViewSet)

urlpatterns = [
    path('api/', include(medical_service_router.urls)),
    path('api/', include(diagnosis_router.urls)),
    path('api/', include(medical_organization_router.urls)),
    path('api/', include(user_router.urls)),
    path("api/user/login", SemdCustomTokenObtainPairView.as_view(), name="token"),
    path("api/user/refresh_token", SemdCustomTokenRefreshView.as_view(), name="refresh_token"),
]

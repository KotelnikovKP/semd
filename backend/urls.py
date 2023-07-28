from django.urls import path, include

from backend.routers import UserRouter, OnlyListRouter, ListRetrieveRouter
from backend.views import UserRegisterViewSet, SemdCustomTokenObtainPairView, SemdCustomTokenRefreshView, \
    MedicalServiceViewSet, DiagnosisViewSet, MedicalOrganizationViewSet, LaboratoryTestViewSet, PatientViewSet

user_router = UserRouter()
user_router.register(r'', UserRegisterViewSet)
medical_service_router = OnlyListRouter()
medical_service_router.register(r'medical_service', MedicalServiceViewSet)
diagnosis_router = OnlyListRouter()
diagnosis_router.register(r'diagnosis', DiagnosisViewSet)
medical_organization_router = OnlyListRouter()
medical_organization_router.register(r'medical_organization', MedicalOrganizationViewSet)
laboratory_test_router = OnlyListRouter()
laboratory_test_router.register(r'laboratory_test', LaboratoryTestViewSet)
patient_router = ListRetrieveRouter()
patient_router.register(r'patient', PatientViewSet)

urlpatterns = [
    path('api/user/', include(user_router.urls)),
    path("api/user/login", SemdCustomTokenObtainPairView.as_view(), name="token"),
    path("api/user/refresh_token", SemdCustomTokenRefreshView.as_view(), name="refresh_token"),
    path('api/ref_inf/', include(medical_service_router.urls)),
    path('api/ref_inf/', include(diagnosis_router.urls)),
    path('api/ref_inf/', include(medical_organization_router.urls)),
    path('api/ref_inf/', include(laboratory_test_router.urls)),
    path('api/', include(patient_router.urls)),
]

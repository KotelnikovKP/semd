from django.urls import path, include

from backend.controllers.ref_inf_views import MedicalServiceViewSet, DiagnosisViewSet, MedicalOrganizationViewSet, \
    LaboratoryTestViewSet
from backend.routers.routers import OnlyListRouter

medical_service_router = OnlyListRouter()
medical_service_router.register(r'medical_service', MedicalServiceViewSet)
diagnosis_router = OnlyListRouter()
diagnosis_router.register(r'diagnosis', DiagnosisViewSet)
medical_organization_router = OnlyListRouter()
medical_organization_router.register(r'medical_organization', MedicalOrganizationViewSet)
laboratory_test_router = OnlyListRouter()
laboratory_test_router.register(r'laboratory_test', LaboratoryTestViewSet)

urlpatterns = [
    path('api/ref_inf/', include(medical_service_router.urls)),
    path('api/ref_inf/', include(diagnosis_router.urls)),
    path('api/ref_inf/', include(medical_organization_router.urls)),
    path('api/ref_inf/', include(laboratory_test_router.urls)),
]

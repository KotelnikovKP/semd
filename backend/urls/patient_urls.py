from django.urls import path, include

from backend.controllers.patient_views import PatientViewSet
from backend.routers.routers import ListRetrieveRouter

patient_router = ListRetrieveRouter()
patient_router.register(r'patient', PatientViewSet)

urlpatterns = [
    path('api/', include(patient_router.urls)),
]

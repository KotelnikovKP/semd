from django.urls import path, include

from backend.views.patient_views import PatientViewSet
from backend.routers.routers import ListRetrieveRouter
from semd.settings import API_PREFIX

patient_router = ListRetrieveRouter()
patient_router.register(r'patient', PatientViewSet)

urlpatterns = [
    path(API_PREFIX, include(patient_router.urls)),
]

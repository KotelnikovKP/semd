from django.urls import path, include

from backend.routers.routers import FullRouter
from backend.views.registry_views import DiagnosisRegistryViewSet, DiagnosisRegistryItemViewSet
from semd.settings import API_PREFIX

diagnosis_registry_router = FullRouter()
diagnosis_registry_router.register(r'diagnosis_registry', DiagnosisRegistryViewSet, basename='diagnosis_registry')

diagnosis_registry_item_router = FullRouter()
diagnosis_registry_item_router.register(r'diagnosis_registry_item', DiagnosisRegistryItemViewSet)

urlpatterns = [
    path(API_PREFIX, include(diagnosis_registry_router.urls)),
    path(API_PREFIX, include(diagnosis_registry_item_router.urls)),
]

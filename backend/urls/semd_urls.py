from django.urls import path, include

from backend.views.semd_views import SEMDViewSet, SemdTestViewSet
from backend.routers.routers import ListRetrieveRouter
from semd.settings import API_PREFIX

semd_router = ListRetrieveRouter()
semd_router.register(r'semd', SEMDViewSet)
semd_test_router = ListRetrieveRouter()
semd_test_router.register(r'semd_test', SemdTestViewSet)

urlpatterns = [
    path(API_PREFIX, include(semd_router.urls)),
    path(API_PREFIX, include(semd_test_router.urls)),
]

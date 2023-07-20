from django.urls import include, path
from rest_framework import routers

from .viewsets import CustomerViewSet

router = routers.DefaultRouter()
router.register(r"customers", CustomerViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

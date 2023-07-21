from django.urls import include, path, re_path
from rest_framework import routers

from .viewsets import PaymentCustomerList, PaymentViewSet

router = routers.DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
    re_path(
        "^payments/customer/(?P<pk>.+)/$",
        PaymentCustomerList.as_view(),
        name="payments-customer",
    ),
]

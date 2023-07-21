from django.urls import include, path, re_path
from rest_framework import routers

from .viewsets import LoanCustomerList, LoanViewSet

router = routers.DefaultRouter()
router.register(r"loans", LoanViewSet)

urlpatterns = [
    path("", include(router.urls)),
    re_path(
        "^loans/customer/(?P<pk>.+)/$",
        LoanCustomerList.as_view(),
        name="loans-customer",
    ),
]

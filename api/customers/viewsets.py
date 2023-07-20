from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.customers.models import Customer

from .serializers import CustomerBalanceSerializer, CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "external_id"

    @action(detail=True, methods=["GET"])
    def balance(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CustomerBalanceSerializer(instance)

        return Response(serializer.data)

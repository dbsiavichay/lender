from rest_framework import generics, viewsets
from rest_framework.serializers import ValidationError

from apps.loans.models import Loan

from .serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = "external_id"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = serializer.validated_data.get("customer")
        outstanding = serializer.validated_data.get("outstanding")

        if outstanding > customer.available_amount:
            raise ValidationError(f"Only availabe {customer.available_amount}")

        return super().create(request, *args, **kwargs)


class LoanCustomerList(generics.ListAPIView):
    serializer_class = LoanSerializer

    def get_queryset(self):
        customer_external_id = self.kwargs["pk"]

        return Loan.objects.filter(customer__external_id=customer_external_id)

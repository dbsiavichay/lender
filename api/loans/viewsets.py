from rest_framework import generics, viewsets

from apps.loans.models import Loan

from .serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = "external_id"


class LoanCustomerList(generics.ListAPIView):
    serializer_class = LoanSerializer

    def get_queryset(self):
        customer_external_id = self.kwargs["pk"]

        return Loan.objects.filter(customer__external_id=customer_external_id)

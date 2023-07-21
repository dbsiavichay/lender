from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from apps.loans.enums import LoanStatus
from apps.payments.enums import PaymentStatus
from apps.payments.models import Payment, PaymentDetail

from .serializers import PaymentCustomerSerializer, PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = "external_id"

    def create(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_ext_id = serializer.validated_data.get("external_id")
        customer = serializer.validated_data.get("customer")
        details = serializer.validated_data.get("details")

        total_amount = sum([d.get("amount") for d in details])

        payment = Payment.objects.create(
            external_id=payment_ext_id, customer=customer, total_amount=total_amount
        )
        reject_payment = False

        for detail in details:
            loan = detail.get("loan")
            amount = detail.get("amount")
            PaymentDetail.objects.create(loan=loan, amount=amount, payment=payment)
            reject_payment = reject_payment or loan.outstanding < amount
            loan.outstanding = loan.outstanding - amount

        if reject_payment:
            payment.status = PaymentStatus.REJECTED
            payment.save(update_fields=["status"])
        else:
            for detail in details:
                loan = detail.get("loan")

                if loan.outstanding == 0:
                    loan.status = LoanStatus.PAID

                loan.save(update_fields=["outstanding", "status"])

        return Response(status=status.HTTP_201_CREATED)


class PaymentCustomerList(generics.ListAPIView):
    serializer_class = PaymentCustomerSerializer

    def get_queryset(self):
        customer_external_id = self.kwargs.get("pk")

        return PaymentDetail.objects.filter(
            payment__customer__external_id=customer_external_id
        )

from rest_framework import serializers

from apps.payments.models import Payment, PaymentDetail


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ["loan", "amount"]


class PaymentSerializer(serializers.ModelSerializer):
    details = PaymentDetailSerializer(many=True)

    class Meta:
        model = Payment
        fields = ["external_id", "customer", "status", "paid_at", "details"]
        read_only_fields = ["status", "paid_at"]


class PaymentCustomerSerializer(serializers.ModelSerializer):
    external_id = serializers.CharField(source="payment.external_id")
    customer_external_id = serializers.CharField(source="payment.customer.external_id")
    loan_external_id = serializers.CharField(source="loan.external_id")
    payment_date = serializers.DateTimeField(source="payment.paid_at")
    status = serializers.IntegerField(source="payment.status")
    total_amount = serializers.DecimalField(
        source="payment.total_amount", max_digits=12, decimal_places=2
    )
    payment_amount = serializers.DecimalField(
        source="amount", max_digits=12, decimal_places=2
    )

    class Meta:
        model = PaymentDetail
        fields = [
            "external_id",
            "customer_external_id",
            "loan_external_id",
            "payment_date",
            "status",
            "total_amount",
            "payment_amount",
        ]

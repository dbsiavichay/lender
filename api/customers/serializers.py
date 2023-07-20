from rest_framework import serializers

from apps.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["external_id", "score", "status"]
        read_only_fields = ["status"]


class CustomerBalanceSerializer(CustomerSerializer):
    class Meta(CustomerSerializer.Meta):
        fields = CustomerSerializer.Meta.fields + ["total_debt", "available_amount"]

from rest_framework import serializers

from apps.loans.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "external_id",
            "amount",
            "outstanding",
            "contract_version",
            "status",
            "customer",
        ]

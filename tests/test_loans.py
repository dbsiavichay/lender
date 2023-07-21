from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey

from apps.customers.models import Customer
from apps.loans.enums import LoanStatus
from apps.loans.models import Loan


class CustomerTest(APITestCase):
    def setUp(self):
        _, key = APIKey.objects.create_key(name="test-service")
        self.api_key = f"Api-Key {key}"
        self.customer = Customer.objects.create(external_id="test_customer", score=5000)

    def test_create_loan(self):
        endpoint = reverse("loan-list")
        data = {
            "external_id": "loan_test",
            "amount": "500.00",
            "outstanding": "500.00",
            "contract_version": "",
            "customer": self.customer.id,
        }
        response = self.client.post(
            endpoint, data, HTTP_AUTHORIZATION=self.api_key, format="json"
        )
        loan = Loan.objects.filter(external_id="loan_test").first()

        self.assertTrue(isinstance(loan, Loan))
        self.assertEqual(loan.status, LoanStatus.ACTIVE)
        self.assertEqual(response.data, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_loan_overindepted(self):
        endpoint = reverse("loan-list")
        data = {
            "external_id": "loan_test",
            "amount": "50000.00",
            "outstanding": "50000.00",
            "contract_version": "",
            "customer": self.customer.id,
        }
        response = self.client.post(
            endpoint, data, HTTP_AUTHORIZATION=self.api_key, format="json"
        )
        loan = Loan.objects.filter(external_id="loan_test").first()

        self.assertIsNone(loan)
        self.assertEqual(str(response.data[0]), "Only availabe 5000.00")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_loans_by_customer(self):
        loan = Loan.objects.create(
            external_id="test_loan",
            amount=1000,
            outstanding=1000,
            customer=self.customer,
        )

        endpoint = reverse("loans-customer", args=[self.customer.external_id])
        response = self.client.get(
            endpoint, HTTP_AUTHORIZATION=self.api_key, format="json"
        )

        data = {
            "external_id": loan.external_id,
            "amount": "1000.00",
            "outstanding": "1000.00",
            "contract_version": loan.contract_version,
            "customer": loan.customer.id,
        }

        self.assertEqual(dict(response.data[0]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

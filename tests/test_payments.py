from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey

from apps.customers.models import Customer
from apps.loans.enums import LoanStatus
from apps.loans.models import Loan
from apps.payments.enums import PaymentStatus
from apps.payments.models import Payment, PaymentDetail


class PaymentTest(APITestCase):
    def setUp(self):
        _, key = APIKey.objects.create_key(name="test-service")
        self.api_key = f"Api-Key {key}"
        self.customer = Customer.objects.create(external_id="test_customer", score=5000)
        self.loan = Loan.objects.create(
            external_id="test_loan",
            amount=1000,
            outstanding=1000,
            customer=self.customer,
        )

    def test_create_payment(self):
        endpoint = reverse("payments-list")
        data = {
            "external_id": "test_payment",
            "customer": self.customer.id,
            "details": [{"loan": self.loan.id, "amount": 500}],
        }
        response = self.client.post(
            endpoint, data, HTTP_AUTHORIZATION=self.api_key, format="json"
        )
        self.loan.refresh_from_db()

        payment = Payment.objects.filter(external_id="test_payment").first()
        payment_detail = payment.details.first()

        self.assertTrue(isinstance(payment, Payment))
        self.assertEqual(payment.total_amount, 500)
        self.assertEqual(payment.status, PaymentStatus.COMPLETED)
        self.assertEqual(payment_detail.amount, 500)
        self.assertEqual(self.loan.outstanding, 500)
        self.assertEqual(self.loan.status, LoanStatus.ACTIVE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_payment_rejected(self):
        endpoint = reverse("payments-list")
        data = {
            "external_id": "test_payment",
            "customer": self.customer.id,
            "details": [{"loan": self.loan.id, "amount": 1500}],
        }
        response = self.client.post(
            endpoint, data, HTTP_AUTHORIZATION=self.api_key, format="json"
        )
        self.loan.refresh_from_db()

        payment = Payment.objects.filter(external_id="test_payment").first()
        payment_detail = payment.details.first()

        self.assertTrue(isinstance(payment, Payment))
        self.assertEqual(payment.total_amount, 1500)
        self.assertEqual(payment.status, PaymentStatus.REJECTED)
        self.assertEqual(payment_detail.amount, 1500)
        self.assertEqual(self.loan.outstanding, 1000)
        self.assertEqual(self.loan.status, LoanStatus.ACTIVE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_payment_total(self):
        endpoint = reverse("payments-list")
        data = {
            "external_id": "test_payment",
            "customer": self.customer.id,
            "details": [{"loan": self.loan.id, "amount": 1000}],
        }
        response = self.client.post(
            endpoint, data, HTTP_AUTHORIZATION=self.api_key, format="json"
        )
        self.loan.refresh_from_db()

        payment = Payment.objects.filter(external_id="test_payment").first()
        payment_detail = payment.details.first()

        self.assertTrue(isinstance(payment, Payment))
        self.assertEqual(payment.total_amount, 1000)
        self.assertEqual(payment.status, PaymentStatus.COMPLETED)
        self.assertEqual(payment_detail.amount, 1000)
        self.assertEqual(self.loan.outstanding, 0)
        self.assertEqual(self.loan.status, LoanStatus.PAID)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_payments_by_customer(self):
        self.client.post(
            reverse("payments-list"),
            {
                "external_id": "test_payment",
                "customer": self.customer.id,
                "details": [{"loan": self.loan.id, "amount": 500}],
            },
            HTTP_AUTHORIZATION=self.api_key,
            format="json",
        )

        payment = PaymentDetail.objects.first()

        endpoint = reverse("payments-customer", args=[self.customer.external_id])
        response = self.client.get(
            endpoint, HTTP_AUTHORIZATION=self.api_key, format="json"
        )

        data = {
            "external_id": payment.payment.external_id,
            "customer_external_id": payment.payment.customer.external_id,
            "loan_external_id": payment.loan.external_id,
            "payment_date": payment.payment.paid_at.strftime("%Y-%m-%d"),
            "status": 1,
            "total_amount": "500.00",
            "payment_amount": "500.00",
        }

        self.assertEqual(dict(response.data[0]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

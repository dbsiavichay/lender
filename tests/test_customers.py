from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.customers.models import Customer


class CustomerTest(APITestCase):
    def test_create_customer(self):
        endpoint = reverse("customer-list")
        data = {"external_id": "test_id", "score": "5000.00"}
        response = self.client.post(endpoint, data, format="json")
        customer = Customer.objects.filter(external_id="test_id").first()

        self.assertTrue(isinstance(customer, Customer))
        self.assertEqual(response.data, {**data, "status": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_customer_detail(self):
        data = {"external_id": "test_id", "score": "5000.00"}
        customer = Customer.objects.create(**data)
        endpoint = reverse("customer-detail", args=[customer.external_id])
        response = self.client.get(endpoint, format="json")

        self.assertEqual(response.data, {**data, "status": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_balance(self):
        data = {"external_id": "test_id", "score": "5000.00"}
        customer = Customer.objects.create(**data)
        endpoint = reverse("customer-balance", args=[customer.external_id])
        response = self.client.get(endpoint, format="json")

        self.assertEqual(
            response.data,
            {**data, "status": 1, "total_debt": 0, "available_amount": 5000},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

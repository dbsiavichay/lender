# Generated by Django 3.2.16 on 2023-07-21 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("customers", "0001_initial"),
        ("loans", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("external_id", models.CharField(max_length=64, unique=True)),
                ("total_amount", models.DecimalField(decimal_places=10, max_digits=20)),
                ("paid_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Completed"), (2, "Rejected")], default=1
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="customers.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PaymentDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=10, max_digits=20)),
                (
                    "loan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="loans.loan"
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="details",
                        to="payments.payment",
                    ),
                ),
            ],
        ),
    ]

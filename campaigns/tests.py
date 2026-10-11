
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Campaign, Task


class TaskLabourCostTests(TestCase):
    def setUp(self):
        self.campaign = Campaign.objects.create(
            name="Test Campaign",
            description="Campaign for labour-cost testing",
        )

    def test_labour_cost_uses_actual_hours(self):
        task = Task.objects.create(
            title="Prepare campaign report",
            campaign=self.campaign,
            estimated_hours=Decimal("6.00"),
            actual_hours=Decimal("4.00"),
            hourly_rate=Decimal("30.00"),
        )

        self.assertEqual(task.labour_cost, Decimal("120.0000"))

    def test_negative_actual_hours_are_rejected(self):
        task = Task(
            title="Invalid task",
            actual_hours=Decimal("-1.00"),
            hourly_rate=Decimal("30.00"),
        )

        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_is_linked_to_campaign(self):
        task = Task.objects.create(
            title="Campaign research",
            campaign=self.campaign,
            estimated_hours=Decimal("2.00"),
            actual_hours=Decimal("2.00"),
            hourly_rate=Decimal("25.00"),
        )

        self.assertEqual(task.campaign, self.campaign)
        self.assertEqual(self.campaign.tasks.count(), 1)

    def test_estimated_hours_are_stored(self):
        task = Task.objects.create(
            title="Plan campaign",
            campaign=self.campaign,
            estimated_hours=Decimal("5.50"),
            actual_hours=Decimal("3.00"),
            hourly_rate=Decimal("20.00"),
        )

        self.assertEqual(task.estimated_hours, Decimal("5.50"))

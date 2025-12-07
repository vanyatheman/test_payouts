from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Payout


class PayoutAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("payouts.tasks.process_payout.delay")
    def test_create_payout_triggers_task(self, mocked_task):
        data = {
            "amount": "150.00",
            "currency": "USD",
            "recipient_details": {"card": 1234_1234_1234_1234},
        }

        response = self.client.post("/api/payouts/", data, format="json")
        self.assertEqual(response.status_code, 201)

        payout_id = response.json()["id"]
        mocked_task.assert_called_once_with(payout_id)

        payout = Payout.objects.get(id=payout_id)
        self.assertEqual(str(payout.amount), "150.00")
        self.assertEqual(payout.currency, "USD")

    def test_patch_status(self):
        p = Payout.objects.create(
            amount=100,
            currency="USD",
            recipient_details={"card": 1234_1234_1234_1234}
        )
        url = f"/api/payouts/{p.id}/"

        response = self.client.patch(
            url, {"status": "completed"}, format="json"
        )
        self.assertEqual(response.status_code, 200)

        p.refresh_from_db()
        self.assertEqual(p.status, Payout.Status.COMPLETED)

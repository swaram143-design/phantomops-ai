import os
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

import healthcare_revenue_api as api
from fastapi import HTTPException
from tools.email_tool import EmailTool


class HealthcareRevenuePilotTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_db_path = api.DB_PATH
        api.DB_PATH = os.path.join(self.temp_dir.name, "pilot.sqlite3")
        api.init_db()

    def tearDown(self):
        api.DB_PATH = self.old_db_path
        self.temp_dir.cleanup()

    def test_enquiry_create_update_and_metrics(self):
        payload = api.EnquiryCreate(
            contact_name="Demo Contact",
            contact_phone="+910000000000",
            service_category="General consultation",
            source="website",
            next_followup_at=datetime(2026, 11, 7, 20, tzinfo=timezone.utc),
        )
        created = api.create_enquiry(payload)
        self.assertEqual(created["status"], "new")

        listing = api.list_enquiries(status="new", limit=10)
        self.assertEqual(listing["count"], 1)
        self.assertEqual(listing["enquiries"][0]["contact_name"], "Demo Contact")

        updated = api.update_enquiry(
            created["id"], api.EnquiryUpdate(status="appointment_booked")
        )
        self.assertTrue(updated["updated"])
        self.assertEqual(updated["status"], "appointment_booked")

        metrics = api.metrics()
        self.assertEqual(metrics["total_enquiries"], 1)
        self.assertEqual(metrics["by_status"]["appointment_booked"], 1)
        self.assertEqual(metrics["followups_due"], 1)

    def test_api_key_is_required_and_checked(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(HTTPException) as missing:
                api.require_api_key("anything")
            self.assertEqual(missing.exception.status_code, 503)

        with patch.dict(os.environ, {"PHANTOMOPS_API_KEY": "test-secret"}):
            with self.assertRaises(HTTPException) as denied:
                api.require_api_key("wrong-secret")
            self.assertEqual(denied.exception.status_code, 401)
            self.assertTrue(api.require_api_key("test-secret"))

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(HTTPException) as error:
            api.update_enquiry("not-real", api.EnquiryUpdate(status="unapproved"))
        self.assertEqual(error.exception.status_code, 400)


class EmailCredentialSafetyTests(unittest.TestCase):
    def test_email_tool_fails_closed_without_environment_credentials(self):
        with patch.dict(os.environ, {}, clear=True):
            tool = EmailTool()
            result = tool.send_email("recipient@example.com", "Test", "Body")
        self.assertFalse(result["success"])
        self.assertIn("not configured", result["error"])

    def test_email_credentials_are_loaded_from_environment(self):
        with patch.dict(
            os.environ,
            {"SMTP_EMAIL": "sender@example.com", "SMTP_PASSWORD": "test-only"},
        ):
            tool = EmailTool()
        self.assertTrue(tool.configured())
        self.assertEqual(tool.email_address, "sender@example.com")
        self.assertEqual(tool.password, "test-only")


if __name__ == "__main__":
    unittest.main()

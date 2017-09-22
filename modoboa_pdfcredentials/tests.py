"""PDF credentials tests."""

import os
import shutil
import tempfile

from modoboa.admin import factories as admin_factories
from modoboa.core import models as core_models
from django.core.urlresolvers import reverse

from modoboa.lib.tests import ModoTestCase


class EventsTestCase(ModoTestCase):
    """Test event handlers."""

    @classmethod
    def setUpTestData(cls):
        """Create some data."""
        super(EventsTestCase, cls).setUpTestData()
        admin_factories.DomainFactory(name="test.com")

    def setUp(self):
        """Create temp. directory to store files."""
        super(EventsTestCase, self).setUp()
        self.workdir = tempfile.mkdtemp()
        self.set_global_parameter("storage_dir", self.workdir)

    def tearDown(self):
        """Reset test env."""
        shutil.rmtree(self.workdir)

    def test_password_updated(self):
        """Check that document is generated at account creation/update."""
        values = {
            "username": "leon@test.com",
            "first_name": "Tester", "last_name": "Toto",
            "role": "SimpleUsers", "quota_act": True,
            "is_active": True, "email": "leon@test.com",
            "random_password": True, "stepid": 2
        }
        self.ajax_post(reverse("admin:account_add"), values)
        fname = os.path.join(self.workdir, "{}.pdf".format(values["username"]))
        self.assertTrue(os.path.exists(fname))
        account = core_models.User.objects.get(username=values["username"])

        # Check if link is present in listing page
        response = self.ajax_get(reverse("admin:_identity_list"))
        self.assertIn('name="get_credentials"', response["rows"])

        # Try to download the file
        response = self.client.get(
            reverse("modoboa_pdfcredentials:account_credentials",
                    args=[account.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

        # File have been deleted?
        self.assertFalse(os.path.exists(fname))

        # Update account
        values.update({"language": "en"})
        self.ajax_post(
            reverse("admin:account_change", args=[account.pk]), values
        )
        self.assertFalse(os.path.exists(fname))

        self.set_global_parameter("generate_at_creation", False)
        self.ajax_post(
            reverse("admin:account_change", args=[account.pk]), values
        )
        self.assertTrue(os.path.exists(fname))

    def test_account_delete(self):
        """Check that document is deleted with account."""
        values = {
            "username": "leon@test.com",
            "first_name": "Tester", "last_name": "Toto",
            "role": "SimpleUsers", "quota_act": True,
            "is_active": True, "email": "leon@test.com",
            "random_password": True, "stepid": 2
        }
        self.ajax_post(reverse("admin:account_add"), values)
        fname = os.path.join(self.workdir, "{}.pdf".format(values["username"]))
        self.assertTrue(os.path.exists(fname))
        account = core_models.User.objects.get(username=values["username"])
        self.ajax_post(
            reverse("admin:account_delete", args=[account.pk]), {}
        )
        self.assertFalse(os.path.exists(fname))

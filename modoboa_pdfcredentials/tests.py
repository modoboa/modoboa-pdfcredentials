"""PDF credentials tests."""

import os
import shutil
import tempfile

from modoboa.admin import factories as admin_factories
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

    def test_account_created(self):
        """Check that document is generated at account creation."""
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

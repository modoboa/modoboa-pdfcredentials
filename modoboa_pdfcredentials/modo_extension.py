"""Generate PDF documents containg account credentials."""

import os

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy, ugettext as _

from modoboa.core.extensions import ModoExtension, exts_pool
from modoboa.lib import events, parameters

from .documents import credentials
from .lib import init_storage_dir, delete_credentials, get_creds_filename

from . import __version__


class PdfCredentials(ModoExtension):

    """Extension declaration."""

    name = "modoboa_pdfcredentials"
    label = ugettext_lazy("PDF credentials")
    version = __version__
    description = ugettext_lazy(
        "Generate PDF documents containing users' credentials"
    )

    def load(self):
        from .app_settings import ParametersForm
        parameters.register(ParametersForm, _("PDF credentials"))

exts_pool.register_extension(PdfCredentials)


@events.observe("PasswordUpdated")
def password_updated(account, raw_password, creation):
    generate_at_creation = parameters.get_admin("GENERATE_AT_CREATION")
    if generate_at_creation == "yes" and not creation:
        return
    if account.role == "SuperAdmins":
        return
    init_storage_dir()
    credentials(account, raw_password)


@events.observe("AccountDeleted")
def account_deleted(account, byuser, **kwargs):
    delete_credentials(account)


@events.observe("ExtraAccountActions")
def extra_account_actions(account):
    fname = get_creds_filename(account)
    if not os.path.exists(fname):
        return []
    return [{
        "name": "get_credentials",
        "url": reverse("modoboa_pdfcredentials:account_credentials",
                       args=[account.id]),
        "img": "fa fa-download",
        "title": _("Retrieve user's credentials as a PDF document")
    }]

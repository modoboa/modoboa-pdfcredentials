import os
from django.utils.translation import ugettext_lazy, ugettext as _
from django.core.urlresolvers import reverse
from modoboa.extensions import ModoExtension, exts_pool
from modoboa.lib import events, parameters
from modoboa.lib.exceptions import ModoboaException
from documents import credentials
from lib import init_storage_dir, delete_credentials, get_creds_filename


class PdfCredentials(ModoExtension):
    name = "modoboa_pdfcredentials"
    label = ugettext_lazy("PDF credentials")
    version = "1.0"
    description = ugettext_lazy("Generate PDF documents containing users' credentials")

    def load(self):
        from app_settings import ParametersForm
        parameters.register(ParametersForm, _("PDF credentials"))

    def destroy(self):
        events.unregister("PasswordUpdated")
        events.unregister("AccountDeleted")
        events.unregister("ExtraAccountActions")
        parameters.unregister()

exts_pool.register_extension(PdfCredentials)


@events.observe("PasswordUpdated")
def password_updated(account, raw_password, creation):
    if parameters.get_admin("GENERATE_AT_CREATION") == "yes" \
        and not creation:
        return
    init_storage_dir()
    credentials(account, raw_password)


@events.observe("AccountDeleted")
def account_deleted(account):
    delete_credentials(account)


@events.observe("ExtraAccountActions")
def extra_account_actions(account):
    fname = get_creds_filename(account)
    if not os.path.exists(fname):
        return []
    return [{
        "name": "get_credentials",
        "url": reverse("modoboa_pdfcredentials.views.get_account_credentials",
                       args=[account.id]),
        "img": "icon-download-alt",
        "title": _("Retrieve user's credentials as a PDF document")
    }]

"""PDF credentials forms."""

from django import forms
from django.utils.translation import ugettext_lazy as _

from modoboa.lib import form_utils
from modoboa.parameters import forms as param_forms


class ParametersForm(param_forms.AdminParametersForm):
    """Admin parameters form."""

    app = "modoboa_pdfcredentials"

    docstore = form_utils.SeparatorField(label=_("Documents storage"))

    storage_dir = forms.CharField(
        label=_("Directory to save documents into"),
        initial="/var/lib/modoboa/pdf_credentials",
        help_text=_("Path to a directory where PDF documents will be saved"),
    )

    security = form_utils.SeparatorField(label=_("Security options"))

    delete_first_dl = form_utils.YesNoField(
        label=_("Delete documents after the first download"),
        initial=True,
        help_text=_(
            "Automatically delete a document just after its first download "
            "from this interface"
        )
    )

    generate_at_creation = form_utils.YesNoField(
        label=_("Generate documents only at account creation"),
        initial=True,
        help_text=_(
            "Generate a new document only when a new account is created. "
            "If set to no, a new document will be created each time a "
            "password is updated."
        )
    )

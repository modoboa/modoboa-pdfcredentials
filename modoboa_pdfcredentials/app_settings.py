"""modoboa_pdfcredentials parameters."""

from django import forms
from django.utils.translation import ugettext_lazy as _

from modoboa.lib.form_utils import SeparatorField, YesNoField
from modoboa.lib.parameters import AdminParametersForm


class ParametersForm(AdminParametersForm):

    """Admin parameters form."""

    app = "modoboa_pdfcredentials"

    docstore = SeparatorField(label=_("Documents storage"))

    storage_dir = forms.CharField(
        label=_("Directory to save documents into"),
        initial="/var/lib/modoboa/pdf_crendentials",
        help_text=_("Path to a directory where PDF documents will be saved"),
    )

    security = SeparatorField(label=_("Security options"))

    delete_first_dl = YesNoField(
        label=_("Delete documents after the first download"),
        initial="yes",
        help_text=_(
            "Automatically delete a document just after its first download "
            "from this interface"
        )
    )

    generate_at_creation = YesNoField(
        label=_("Generate documents only at account creation"),
        initial="yes",
        help_text=_(
            "Generate a new document only when a new account is created. "
            "If set to no, a new document will be created each time a "
            "password is updated."
        )
    )

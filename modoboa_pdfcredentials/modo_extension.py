"""Generate PDF documents containg account credentials."""

from django.utils.translation import ugettext_lazy

from modoboa.core.extensions import ModoExtension, exts_pool
from modoboa.parameters import tools as param_tools

from . import __version__
from . import forms


class PdfCredentials(ModoExtension):
    """Extension declaration."""

    name = "modoboa_pdfcredentials"
    label = ugettext_lazy("PDF credentials")
    version = __version__
    description = ugettext_lazy(
        "Generate PDF documents containing users' credentials"
    )

    def load(self):
        param_tools.registry.add(
            "global", forms.ParametersForm, ugettext_lazy("PDF credentials"))


exts_pool.register_extension(PdfCredentials)

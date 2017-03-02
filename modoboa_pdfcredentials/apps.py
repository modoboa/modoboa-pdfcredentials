"""AppConfig for PDF credentials."""

from django.apps import AppConfig


class PDFCredentialsConfig(AppConfig):
    """App configuration."""

    name = "modoboa_pdfcredentials"
    verbose_name = "PDF credentials for Modoboa"

    def ready(self):
        from . import handlers

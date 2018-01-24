# -*- coding: utf-8 -*-

"""Generate PDF documents containing user credentials."""

from __future__ import unicode_literals

from pkg_resources import get_distribution, DistributionNotFound


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass

default_app_config = "modoboa_pdfcredentials.apps.PDFCredentialsConfig"

"""modoboa_pdfcredentials views."""

import os

from rfc6266 import build_header

from django.http import HttpResponse
from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import (
    login_required, permission_required
)

from modoboa.core.models import User
from modoboa.lib.exceptions import ModoboaException, PermDeniedException
from modoboa.lib import parameters

from .lib import decrypt_file, get_creds_filename


@login_required
@permission_required("core.add_user")
def get_account_credentials(request, accountid):
    """View to download a document."""
    account = User.objects.get(pk=accountid)
    if not request.user.can_access(account):
        raise PermDeniedException()
    fname = get_creds_filename(account)
    if not os.path.exists(fname):
        raise ModoboaException(_("No document available for this user"))
    content = decrypt_file(fname)
    if parameters.get_admin("DELETE_FIRST_DL") == "yes":
        os.remove(fname)
    resp = HttpResponse(content)
    resp["Content-Type"] = "application/pdf"
    resp["Content-Length"] = len(content)
    resp["Content-Disposition"] = build_header(os.path.basename(fname))
    return resp

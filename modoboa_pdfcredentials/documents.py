"""The code used to generate PDF files (based on Reportlab."""

from io import BytesIO
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import utils
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.sites.models import Site

from .lib import crypt_and_save_to_file, get_creds_filename

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='Footer', alignment=TA_CENTER, fontName="Helvetica-Oblique",
    textColor=colors.lightgrey
))


def resized_image(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def credentials(account, password):
    """Generate a PDF document containing account credentials."""

    def page_template(canvas, doc):
        canvas.setTitle(_("Personal account information"))
        canvas.setAuthor(account.fullname)
        canvas.setCreator("Modoboa")
        footer = [Paragraph(_("Powered by Modoboa - Mail hosting made simple"),
                            styles["Footer"])]
        Frame(0, 0, 21 * cm, 4 * cm).addFromList(footer, canvas)

    filename = get_creds_filename(account)
    buff = BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=A4)
    story = []
    imgpath = os.path.join(settings.STATIC_ROOT, "css")
    story.append(resized_image(imgpath + "/modoboa.png", 6*cm))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(_("Personal account information"), styles["Title"]))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph(_("""
Dear %s, this document contains the credentials you will need
to connect to Modoboa. Learn the content and destroy
the document as soon as possible.
""") % account.fullname, styles["Normal"]))
    url = "http(s)://{}{}".format(
        Site.objects.get_current().domain, settings.LOGIN_URL)
    data = [
        ["URL", url],
        [_("Username"), account.username],
        [_("Password"), password]
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        # ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ]))
    story.append(Spacer(1, 2 * cm))
    story.append(table)

    doc.build(story, onFirstPage=page_template, onLaterPages=page_template)
    length = len(buff.getvalue())
    buff.seek(0)
    crypt_and_save_to_file(buff, filename, length)

"""The code used to generate PDF files (based on Reportlab)"""

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

from . import lib

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='Footer', alignment=TA_CENTER, fontName="Helvetica-Oblique",
    textColor=colors.lightgrey
))
styles.add(ParagraphStyle(
    name='Warning', fontName="Helvetica-Oblique",
    textColor=colors.red, fontSize=12
))
styles.add(ParagraphStyle(
    name='Link',
    textColor=colors.blue
))
styles.add(ParagraphStyle(
    name='Greeting', alignment=TA_CENTER, fontName="Helvetica-Oblique",
    fontSize=14
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
        Frame(0, 0, 21 * cm, 2 * cm).addFromList(footer, canvas)

    filename = lib.get_creds_filename(account)
    buff = BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=A4)

    story = []

    story.append(resized_image(lib.get_document_logo(), 8*cm))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(_("Personal account information"), styles["Title"]))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(_("""
Dear %s, this document contains the credentials you will need
to connect to Modoboa. Learn the content and destroy
the document as soon as possible.
""") % account.fullname, styles["Normal"]))

    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(_("Webinterface:"), styles["h3"]))

    url = "https://{}".format(
        Site.objects.get_current().domain)
    data = [
        ["URL", url],
        [_("Username"), account.username],
        [_("Password"), password]
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (1, 0), (1, 0), colors.blue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    ]))
    story.append(table)

    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(_("""
Here you can view your emails anytime online and check the spam filter and settings.
"""), styles["Normal"]))

    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(_("Please change your password now!"), styles["Warning"]))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(_("Installation PC/Tablet/Smartphone:"), styles["h3"]))

    story.append(Spacer(1, 0.2 * cm))
    data = [
        [_("Username"), account.username],
        [_("Password"), password],
        ["Type", "IMAP"],
        ["IMAP-Server (Inbox)", account.username.split("@")[1] ],
        ["Security", "SSL"],
        ["Port", "993"],
        ["SMTP-Server (Outbox)", account.username.split("@")[1] ],
        ["Security", "TLS"],
        ["Port", "587"],
        ["Requires Auth?", "Yes (use same as Inbox)"],
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        # ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ]))
    story.append(table)

    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(_("Use this credentials for your computer. tablet or phone"), styles["Normal"]))

    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph(_("Have fun with you new email account! :-)"), styles["Greeting"]))

    doc.build(story, onFirstPage=page_template, onLaterPages=page_template)
    length = len(buff.getvalue())
    buff.seek(0)
    lib.crypt_and_save_to_file(buff, filename, length)

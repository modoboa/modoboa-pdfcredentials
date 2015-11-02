"""Internal library."""

from io import BytesIO
import os
import random
import struct

from Crypto.Cipher import AES

from django.utils.translation import ugettext as _

from modoboa.lib import parameters
from modoboa.lib.exceptions import InternalError


def init_storage_dir():
    """Create the directory whare documents will be stored."""
    storage_dir = parameters.get_admin("STORAGE_DIR")
    if os.path.exists(storage_dir):
        return
    try:
        os.mkdir(storage_dir)
    except (OSError, IOError) as inst:
        raise InternalError(
            _("Failed to create the directory that will contain "
              "PDF documents (%s)") % inst
        )


def get_creds_filename(account):
    """Return the full path of a document."""
    storage_dir = parameters.get_admin("STORAGE_DIR")
    return os.path.join(storage_dir, account.username + ".pdf")


def delete_credentials(account):
    """Try to delete a local file."""
    fname = get_creds_filename(account)
    if not os.path.exists(fname):
        return
    try:
        os.remove(fname)
    except OSError:
        pass


def crypt_and_save_to_file(content, filename, length, chunksize=64*1024):
    """Crypt content and save it to a file."""
    key = parameters.get_admin("SECRET_KEY", app="core")
    iv = "".join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    with open(filename, 'wb') as fp:
        fp.write(struct.pack('<Q', length))
        fp.write(iv)
        while True:
            chunk = content.read(chunksize)
            if not len(chunk):
                break
            elif len(chunk) % 16:
                chunk += ' ' * (16 - len(chunk) % 16)
            fp.write(encryptor.encrypt(chunk))


def decrypt_file(filename, chunksize=24*1024):
    """Decrypt the content of a file and return it."""
    buff = BytesIO()
    key = parameters.get_admin("SECRET_KEY", app="core")
    with open(filename, 'rb') as fp:
        origsize = struct.unpack('<Q', fp.read(struct.calcsize('Q')))[0]
        iv = fp.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        while True:
            chunk = fp.read(chunksize)
            if not len(chunk):
                break
            buff.write(decryptor.decrypt(chunk))
        buff.truncate(origsize)
    return buff.getvalue()

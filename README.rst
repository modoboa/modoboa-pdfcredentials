PDF credentials for Modoboa
===========================

|gha| |codecov|

A simple `Modoboa <http://modoboa.org/>`_ extension which provides a
way to download PDF documents containing users credentials.

Installation
------------

Install this extension system-wide or inside a virtual environment by
running the following command::

  $ python setup.py install

Then, edit the ``settings.py`` file of your modoboa instance and
add ``modoboa_pdfcredentials`` inside the ``MODOBOA_APPS`` variable
like this::

  MODOBOA_APPS = (
    # ...
    'modoboa_pdfcredentials',
  )

Restart the python process running modoboa (uwsgi, gunicorn, apache,
whatever).

Configuration
-------------

All the configuration is done from the admin panel (*Modoboa >
Parameters > PDF Credentials*).

.. |gha| image:: https://github.com/modoboa/modoboa-pdfcredentials/actions/workflows/plugin.yml/badge.svg
   :target: https://github.com/modoboa/modoboa-pdfcredentials/actions/workflows/plugin.yml
.. |codecov| image:: https://codecov.io/gh/modoboa/modoboa-pdfcredentials/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/modoboa/modoboa-pdfcredentials

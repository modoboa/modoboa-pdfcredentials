PDF credentials for Modoboa
===========================

|travis| |codecov| |landscape|

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

.. |travis| image:: https://travis-ci.org/modoboa/modoboa-pdfcredentials.svg?branch=master
   :target: https://travis-ci.org/modoboa/modoboa-pdfcredentials

.. |codecov| image:: https://codecov.io/gh/modoboa/modoboa-pdfcredentials/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/modoboa/modoboa-pdfcredentials

.. |landscape| image:: https://landscape.io/github/modoboa/modoboa-pdfcredentials/master/landscape.svg?style=flat
   :target: https://landscape.io/github/modoboa/modoboa-pdfcredentials/master
   :alt: Code Health

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'modoboa_pdfcredentials.views',

    url(r'^credentials/(?P<accountid>\d+)/$', 'get_account_credentials',
        name="account_credentials"),
)

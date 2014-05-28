from django.conf.urls import patterns

urlpatterns = patterns(
    'modoboa_pdfcredentials.views',
    (r'^credentials/(?P<accountid>\d+)/$', 'get_account_credentials'),
)

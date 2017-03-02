from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^credentials/(?P<accountid>\d+)/$', views.get_account_credentials,
        name="account_credentials"),
]

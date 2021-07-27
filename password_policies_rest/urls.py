import logging

from django.conf.urls import url

from . import views as api_views

logger = logging.getLogger(__name__)

app_name = "password-policies-rest"


urlpatterns = [
    url(r'^change-password/$',
        api_views.ChangePasswordCheckAPIView.as_view(),
        name="change-password-api"),
]

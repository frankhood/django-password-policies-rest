import logging

from django.urls import path

from . import views as api_views

logger = logging.getLogger(__name__)

app_name = "password-policies-rest"


urlpatterns = [
    path(
        "change-password/",
        api_views.ChangePasswordCheckAPIView.as_view(),
        name="change-password-api",
    ),
]

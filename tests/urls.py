from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    # PASSWORDS - Part 1
    re_path(
        r"^admin/password_change/",
        RedirectView.as_view(pattern_name="password_change", permanent=False),
    ),
    re_path(r"^admin/", admin.site.urls),
    # PASSWORDS - Part 2
    path("admin/password/", include("password_policies.urls")),
    # PASSWORD REST
    path("api/password-policies/", include("password_policies_rest.urls")),
]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include, path
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    # PASSWORDS - Part 1
    path('admin/password_change/', RedirectView.as_view(pattern_name="password_change", permanent=False)),
    url(r'^admin/', admin.site.urls),
    # PASSWORDS - Part 2
    path('admin/password/', include('password_policies.urls')),
    # PASSWORD REST
    path('api/password-policies/',
       include('password_policies_rest.urls')),
]

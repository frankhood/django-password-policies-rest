=====
Usage
=====

Install Password Policies Rest

Add these packages in your requirements.txt:

.. code-block:: bash

    git+https://github.com/frankhood/django-password-policies-iplweb.git@develop#egg=django-password-policies-iplweb
    git+https://github.com/frankhood/django-password-policies-rest.git@develop#egg=django-password-policies-rest
    python-Levenshtein==0.12.2


Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'password_policies',
        'password_policies_rest',
        ...
    )

Add password_policies's MIDDLEWARE:

.. code-block:: python

    MIDDLEWARE = (
        ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'password_policies.middleware.PasswordChangeMiddleware',
        ...
    )



Add Password Policies's and Password Policies Rest's URL patterns:

.. code-block:: python

    from password_policies_rest import urls as password_policies_rest_urls


    urlpatterns = [
        ...
        # PASSWORDS - PART 1
        url(r'^admin/password_change/', RedirectView.as_view(pattern_name="password_change", permanent=False)),
        # Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),
        # PASSWORDS - Part 2
        url(r'^admin/password/', include('password_policies.urls')),

        # PASSWORDS-REST
        url(r'^api/password-policies/', include('project.apps.password_policies_rest.urls')),
        ...
    ]


Update your DB::

    ./manage.py migrate



Modify templates

Insert these templates in the project's directory `templates`

1. `registration/password_change_form.html` :

.. code-block:: jinja

    {% extends "password_policies_rest/password_change_form.html" %}

2. `registration/password_change_other_user_form.html` :

.. code-block:: jinja

    {% extends 'password_policies_rest/password_change_form.html' %}

    {% block head_text %}{% endblock %}



Override UserAdmin

Modify default UserAdmin to change "change_user_password_template" template and form

.. code-block:: python

    from django.contrib.auth import get_user_model
    from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

    from password_policies.forms import PasswordPoliciesForm

    class UserAdmin(DjangoUserAdmin):
       change_user_password_template = "registration/password_change_other_user_form.html"
       change_password_form = PasswordPoliciesForm

    # admin.site.unregister(get_user_model())  # if you are not handling your User Model
    admin.site.register(get_user_model(), UserAdmin)

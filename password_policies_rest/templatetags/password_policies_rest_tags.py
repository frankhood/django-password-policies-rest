import json

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, ngettext
from password_policies.conf import settings as password_settings
from password_policies.forms import validators

register = template.Library()


@register.simple_tag(takes_context=False)
def get_password_policies_checks():
    # DYNAMIC CHECKS
    password_dynamic_checks = {}
    if password_settings.PASSWORD_MIN_LENGTH:
        password_dynamic_checks.update(
            {
                "min_length": ngettext(
                    "must be at least 1 character long",
                    "must be at least %(count)s characters long",
                    password_settings.PASSWORD_MIN_LENGTH,
                )
                % {"count": password_settings.PASSWORD_MIN_LENGTH}
            }
        )
    if password_settings.PASSWORD_COMMON_SEQUENCES:
        password_dynamic_checks.update(
            {
                validators.CommonSequenceValidator.code: gettext(
                    "must not be a common sequence of characters"
                )
            }
        )
    if password_settings.PASSWORD_MAX_CONSECUTIVE:
        password_dynamic_checks.update(
            {
                validators.ConsecutiveCountValidator.code: gettext(
                    "must not contain %(count)s or more consecutive identical characters"
                )
                % {"count": password_settings.PASSWORD_MAX_CONSECUTIVE}
            }
        )
    if password_settings.PASSWORD_USE_CRACKLIB:
        password_dynamic_checks.update(
            {validators.CracklibValidator.code: gettext("must be strong enough.")}
        )
    if password_settings.PASSWORD_DICTIONARY:
        password_dynamic_checks.update(
            {
                validators.DictionaryValidator.code: gettext(
                    "must not be based on a dictionary word."
                )
            }
        )
    if password_settings.PASSWORD_MIN_LETTERS:
        password_dynamic_checks.update(
            {
                validators.LetterCountValidator.code: ngettext(
                    "must contain at least 1 alphanumeric character",
                    "must contain at least %(count)s alphanumeric characters",
                    password_settings.PASSWORD_MIN_LETTERS,
                )
                % {"count": password_settings.PASSWORD_MIN_LETTERS}
            }
        )
    if password_settings.PASSWORD_MIN_LOWERCASE_LETTERS:
        password_dynamic_checks.update(
            {
                validators.LowercaseLetterCountValidator.code: ngettext(
                    "must contain at least 1 lowercase character",
                    "must contain at least %(count)s lowercase characters",
                    password_settings.PASSWORD_MIN_LOWERCASE_LETTERS,
                )
                % {"count": password_settings.PASSWORD_MIN_LOWERCASE_LETTERS}
            }
        )
    if password_settings.PASSWORD_MIN_UPPERCASE_LETTERS:
        password_dynamic_checks.update(
            {
                validators.UppercaseLetterCountValidator.code: ngettext(
                    "must contain at least 1 uppercase character",
                    "must contain at least %(count)s uppercase characters",
                    password_settings.PASSWORD_MIN_UPPERCASE_LETTERS,
                )
                % {"count": password_settings.PASSWORD_MIN_UPPERCASE_LETTERS}
            }
        )
    if password_settings.PASSWORD_MIN_NUMBERS:
        password_dynamic_checks.update(
            {
                validators.NumberCountValidator.code: ngettext(
                    "must contain at least 1 number",
                    "must contain at least %(count)s numbers",
                    password_settings.PASSWORD_MIN_NUMBERS,
                )
                % {"count": password_settings.PASSWORD_MIN_NUMBERS}
            }
        )
    if password_settings.PASSWORD_MIN_SYMBOLS:
        password_dynamic_checks.update(
            {
                validators.SymbolCountValidator.code: ngettext(
                    "must contain at least 1 special character (e.g. @#$%%^&.)",
                    "must contain at least %(count)s special characters (e.g. @#$%%^&.)",
                    password_settings.PASSWORD_MIN_SYMBOLS,
                )
                % {"count": password_settings.PASSWORD_MIN_SYMBOLS}
            }
        )
    password_dynamic_checks.update(
        {validators.NotEmailValidator.code: gettext("must not be an email.")}
    )

    # STATIC CHECKS
    password_static_checks = {}
    if (
        password_settings.PASSWORD_USE_HISTORY
        and password_settings.PASSWORD_HISTORY_COUNT
    ):
        password_static_checks.update(
            {
                "password_used": ngettext(
                    "Make sure it differs from the last password",
                    "Make sure it differs from the last %(count)s passwords",
                    password_settings.PASSWORD_HISTORY_COUNT,
                )
                % {"count": password_settings.PASSWORD_HISTORY_COUNT}
            }
        )
    else:
        password_static_checks.update(
            {"password_used": gettext("Make sure it differs from the last password")}
        )
    if password_settings.PASSWORD_DIFFERENCE_DISTANCE:
        try:
            pass

            password_static_checks.update(
                {
                    "password_similar": gettext(
                        "Make sure it is not similar to the old password"
                    )
                }
            )
        except ImportError:
            pass

    # i18n_tokens
    i18n_tokens = {
        "passwordOk": gettext("Password ok!"),
        "oldPassEmpty": gettext("Old password is required"),
        "passwordNotTwins": gettext("Passwords do not match"),
        "passwordTwins": gettext("Password match!"),
        "passwordNotStrong": gettext(
            "must be strong enough"
        ),  # this is the fallback message
    }

    return mark_safe(
        json.dumps(
            {
                "prefix": gettext(
                    "The new password must have the following characteristics:"
                ),
                "checks": password_dynamic_checks,
                "static_checks": password_static_checks,
                "i18n": i18n_tokens,
            }
        )
    )

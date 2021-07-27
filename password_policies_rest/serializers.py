import six
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _
from password_policies.conf import settings as password_settings
from password_policies.forms import validators as password_validators
from rest_framework import serializers
from rest_framework.compat import MaxLengthValidator, MinLengthValidator
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty, get_error_detail
from rest_framework.serializers import as_serializer_error

User = get_user_model()


class PasswordPoliciesSerializer(serializers.Serializer):
    """
    A serializer that lets a user set his/her password without entering the
    old password.

    Has the following fields and methods:"""

    #: This forms error messages.
    default_error_messages = dict(
        **{
            "password_used": _(
                "The new password was used before. " "Please enter another one."
            ),
        }
    )

    new_password_validators = [
            password_validators.validate_common_sequences,
            password_validators.validate_consecutive_count,
            password_validators.validate_cracklib,
            password_validators.validate_dictionary_words,
            password_validators.validate_letter_count,
            password_validators.validate_lowercase_letter_count,
            password_validators.validate_uppercase_letter_count,
            password_validators.validate_number_count,
            password_validators.validate_symbol_count,
            password_validators.validate_entropy,
            password_validators.validate_not_email,
            MaxLengthValidator(password_settings.PASSWORD_MAX_LENGTH or 1000, message=lazy(
                serializers.CharField.default_error_messages['max_length'].format,
                six.text_type
            )(max_length=password_settings.PASSWORD_MAX_LENGTH or 1000)),
            MinLengthValidator(password_settings.PASSWORD_MIN_LENGTH or 0, message=lazy(
                serializers.CharField.default_error_messages['min_length'].format,
                six.text_type
            )(min_length=password_settings.PASSWORD_MIN_LENGTH or 0))
        ]

    new_password1 = serializers.CharField(
        label=_("New password"),
        write_only=True, required=True, allow_blank=False, allow_null=False,
        style={'input_type': 'password'},
    )

    def fail_lazy(self, code):
        if not hasattr(self, '_lazy_errors'):
            self._lazy_errors = []
        try:
            self.fail(code)
        except ValidationError as ex:
            self._lazy_errors.extend(ex.detail)

    def validate(self, validated_data):
        """
        Validates that old and new password are not too similar."""
        # old_password = validated_data.get("old_password")
        self._lazy_errors = getattr(self, "_lazy_errors", [])
        try:
            self.run_validators(validated_data)
        except (ValidationError) as ex:
            self._lazy_errors.extend(ex.detail)
        except DjangoValidationError as ex:
            self._lazy_errors.extend(get_error_detail(ex))
        new_password = validated_data.get("new_password1")

        for new_password_validator in self.new_password_validators:
            try:
                new_password_validator(new_password)
            except (ValidationError) as ex:
                self._lazy_errors.extend(ex.detail)
            except DjangoValidationError as ex:
                self._lazy_errors.extend(get_error_detail(ex))

        return validated_data

    def run_validation(self, data=empty):
        value = super().run_validation(data=data)
        if getattr(self, "_lazy_errors", []):
            raise ValidationError(detail=as_serializer_error(ValidationError(self._lazy_errors)))
        return value

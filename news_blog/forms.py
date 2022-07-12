from django import forms
from django.core.exceptions import ValidationError
from .models import ApplicationNotification
from news_blog.constants import (
    CHECK_BOX_LABEL,
    ALREADY_ONE_ROLE_EXISTS,
    ALREADY_APPLIED_FOR__ROLE,
    NOTIFICATION_TYPE_MANAGER_REQUEST,
    NOTIFICATION_STATUS_REJECTED, NOTIFICATION_TYPE_EDITOR_REQUEST, ALREADY_PREMIUM_USER
)
from users.constants import (
    USER_TYPE_CONSUMER,
    USER_TYPE_EDITOR,
    USER_TYPE_MANAGER
)


class ManagerApplicationForm(forms.Form):
    check = forms.BooleanField(label=CHECK_BOX_LABEL, required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        print(kwargs)
        super(ManagerApplicationForm, self).__init__(*args, **kwargs)

    def clean_check(self):
        data = self.cleaned_data['check']
        current_user = self.request.user

        # If user is already a manager or editor
        if current_user.user_type.name != USER_TYPE_CONSUMER:
            raise ValidationError(ALREADY_ONE_ROLE_EXISTS % current_user.user_type.name)

        # If already applied for current submitted role
        application_notification = ApplicationNotification.objects.filter(user=current_user)
        if application_notification.filter(notification_type__name=NOTIFICATION_TYPE_MANAGER_REQUEST).exists():
            raise ValidationError(
                ALREADY_APPLIED_FOR__ROLE % (
                    USER_TYPE_MANAGER,
                    application_notification.first().status
                )
            )

        # If already applied for other role
        if (application_notification.exists() and
                application_notification.first().status.name != NOTIFICATION_STATUS_REJECTED):
            raise ValidationError(
                ALREADY_APPLIED_FOR__ROLE % (
                    USER_TYPE_EDITOR,
                    application_notification.first().status
                )
            )
        return data


class EditorApplicationForm(forms.Form):
    check = forms.BooleanField(label=CHECK_BOX_LABEL, required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EditorApplicationForm, self).__init__(*args, **kwargs)

    def clean_check(self):
        data = self.cleaned_data['check']
        current_user = self.request.user

        # If user is already a manager or editor
        if current_user.user_type.name != USER_TYPE_CONSUMER:
            raise ValidationError(ALREADY_ONE_ROLE_EXISTS % current_user.user_type.name)

        # If already applied for current submitted role
        application_notification = ApplicationNotification.objects.filter(user=current_user)
        if application_notification.filter(notification_type__name=NOTIFICATION_TYPE_EDITOR_REQUEST).exists():
            raise ValidationError(
                ALREADY_APPLIED_FOR__ROLE % (
                    USER_TYPE_EDITOR,
                    application_notification.first().status
                )
            )

        # If already applied for other role
        if (application_notification.exists() and
                application_notification.first().status.name != NOTIFICATION_STATUS_REJECTED):
            raise ValidationError(
                ALREADY_APPLIED_FOR__ROLE % (
                    USER_TYPE_MANAGER,
                    application_notification.first().status
                )
            )
        return data

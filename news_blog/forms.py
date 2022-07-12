from django import forms
from django.core.exceptions import ValidationError
from .models import NotificationType, ApplicationNotification
from users.models import UserType
from news_blog.constants import (
    CHECK_BOX_LABEL,
    ALREADY_ONE_ROLE_EXISTS,
    ALREADY_APPLIED_FOR__ROLE,
    NOTIFICATION_TYPE_MANAGER_REQUEST,
    NOTIFICATION_STATUS_REJECTED
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
    check = forms.BooleanField(label='I have read and agree the terms and conditions.', required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EditorApplicationForm, self).__init__(*args, **kwargs)

    def clean_check(self):
        data = self.cleaned_data['check']
        current_user = self.request.user

        # if user is already a manager or editor
        consumer_type_obj = UserType.objects.get(name='consumer')
        if current_user.user_type != consumer_type_obj:
            raise ValidationError(
                f"You cannot apply because you already have one role as {current_user.user_type.name}"
            )

        # if already applied for current submited role
        notification_type = NotificationType.objects.get(name='editor request')
        application_notification = ApplicationNotification.objects.filter(
            user=current_user,
            notification_type=notification_type
        )

        if application_notification.exists():
            raise ValidationError(
                f"You have already applied for editor. Current status: {application_notification.first().status}"
            )

        # if already applied for other role
        application_notification = ApplicationNotification.objects.filter(
            user=current_user
        )

        if application_notification.exists() and application_notification.first().status.name != 'rejected':
            role = application_notification.first().notification_type.name.split()[0]
            raise ValidationError(
                f"You have already applied for {role}."
            )
        return data


class PremiumApplicationForm(forms.Form):
    check = forms.BooleanField(label='I have read and agree the terms and conditions.', required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PremiumApplicationForm, self).__init__(*args, **kwargs)

    def clean_check(self):
        check = self.cleaned_data['check']
        current_user = self.request.user

        if current_user.is_premium_user:
            raise ValidationError(
                f"You cannot apply because you already are premium user."
            )

        return check

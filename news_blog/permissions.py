from django.core.exceptions import PermissionDenied


class GroupRequiredMixin(object):
    """
        group_required - list of strings, required param
    """

    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            user_groups = []
            for group in request.user.groups.values_list('name', flat=True):
                user_groups.append(group)
            if len(set(user_groups).intersection(self.group_required)) <= 0:
                raise PermissionDenied
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)


class CheckPremiumUserMixin(object):
    required = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_premium_user:
            raise PermissionDenied
        return super(CheckPremiumUserMixin, self).dispatch(request, *args, **kwargs)

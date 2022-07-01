
def get_paginated_context(context, request, queryset, paginator_class, paginate_by):
    page = request.GET.get('page', 1)
    paginator = paginator_class(queryset, paginate_by)

    objects = paginator.page(page)
    objects.adjusted_elided_pages = paginator.get_elided_page_range(page)
    context['page_obj'] = objects

    return context


def is_mark_seen_success(request, notification_class):
    notification_id = request.GET.get('pk', '')
    notifications = notification_class.objects.filter(id=notification_id)
    if not notifications.exists():
        return False

    notification = notifications.first()
    notification.seen = True
    notification.save()
    return True


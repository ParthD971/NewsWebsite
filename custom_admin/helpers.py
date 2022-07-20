from datetime import datetime
from news_blog.constants import DEFAULT_IMAGE_NAME
from django.db.models import Q


def get_queryset_for_created_on(request, queryset):
    """This function checks for date of create and if it exists then filter queryset accordingly."""
    created_on = request.GET.get('created_on', '').strip()
    if created_on:
        created_on = datetime.strptime(created_on, '%Y-%m-%d').date()
        return queryset.filter(created_on=created_on)
    return queryset


def get_queryset_for_categories(request, queryset, categories):
    """This function checks for category and if it exists then filter queryset accordingly."""
    lis = [cat.name for cat in categories if request.GET.get(cat.name, '').strip()]
    if lis:
        return queryset.filter(category__name__in=lis).distinct()
    return queryset


def remove_and_update_image_for_post(old_post_obj):
    """This function check for image existence and delete it.."""
    if old_post_obj.image and old_post_obj.image.url.split('/')[-1] != DEFAULT_IMAGE_NAME:
        old_post_obj.image.delete(False)


def get_queryset_for_deleted_on(request, queryset):
    """This function checks for date of delete and if it exists then filter queryset accordingly."""
    deleted_on = request.GET.get('deleted_on', '')
    if deleted_on:
        deleted_on = datetime.strptime(deleted_on, '%Y-%m-%d').date()
        return queryset.filter(recycle_created_on=deleted_on)
    return queryset


def get_queryset_for_search(request, queryset):
    """This function checks for search parameter and if it exists then filter queryset accordingly."""
    search = request.GET.get('search', '')
    if search.strip():
        return queryset.filter(Q(post__title__contains=search) | Q(post__content__contains=search))
    return queryset

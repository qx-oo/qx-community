from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from qx_base.qx_core.models import ContentTypeRelated


class QxComment(ContentTypeRelated):
    '''
    Comment
    ---
    type_map_model = {
        "video": "test.Video",
        "audio": "test.audio",
    }
    '''

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="用户", on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="被回复用户",
        related_name='to_user_comments', null=True, default=None,
        on_delete=models.CASCADE)
    content = models.TextField(
        verbose_name="内容", null=False, blank=False)
    parent = models.ForeignKey(
        'self', verbose_name="父级评论", null=True, default=None,
        on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name="是否可用", default=True)
    created = models.DateTimeField(
        verbose_name='创建时间', default=timezone.now, editable=False)

    class Meta:
        abstract = True


class QxStar_Meta:
    verbose_name = "点赞"
    unique_together = (("user", "object_id", "type"),)


class QxStar(ContentTypeRelated):
    '''
    Star
    ---
    type_map_model = {
        "video": "test.Video",
        "audio": "test.audio",
    }
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="用户", on_delete=models.CASCADE)
    created = models.DateTimeField(
        verbose_name='创建时间', default=timezone.now, editable=False)

    class Meta:
        abstract = True


class QxPost(ContentTypeRelated):
    """
    Post
    ---
    type_map_model = {
        "video": "test.Video",
        "audio": "test.audio",
    }
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="用户", on_delete=models.CASCADE)
    created = models.DateTimeField(
        verbose_name='创建时间', default=timezone.now, editable=False)
    info = JSONField(
        verbose_name="详细信息", default=dict)
    is_active = models.BooleanField(
        verbose_name="是否可用", default=True)

    class Meta:
        abstract = True

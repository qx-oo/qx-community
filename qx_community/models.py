from django.apps import apps
from django.db import models, connection
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from qx_base.qx_core.models import (
    ContentTypeRelated, load_set_queryset_object
)


class QxStarMixin(models.Model):

    star = models.PositiveIntegerField(
        verbose_name="点赞数", default=0)

    class Meta:
        abstract = True


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

    def _update_type_model_star(self):
        type_model = self.type_map_model.get(self.type)
        if type_model and isinstance(type_model, QxStarMixin):
            with connection.cursor() as cursor:
                sql = """
                UPDATE {type_model} SET star=(
                    SELECT COUNT(*) FROM {star_model}
                    WHERE type={type} AND object_id={object_id}
                )
                WHERE id={object_id}
                """.format(
                    type_model=type_model._meta.db_table,
                    star_model=self._meta.db_table,
                    type=self.type,
                    object_id=self.object_id,
                )
                cursor.execute(sql)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_type_model_star()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self._update_type_model_star()

    class Meta:
        abstract = True


class QxComment(ContentTypeRelated, QxStarMixin):
    '''
    Comment
    ---
    type_map_model = {
        "video": "test.Video",
        "audio": "test.Audio",
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

    @classmethod
    def load_user(cls, queryset):
        User = apps.get_model(settings.AUTH_USER_MODEL)
        return load_set_queryset_object(
            queryset, User, {'user_id': 'user', 'to_user_id': 'to_user'},
            select_related=['userinfo'])

    class Meta:
        abstract = True


class QxStar_Meta:
    verbose_name = "点赞"
    unique_together = (("user", "object_id", "type"),)


class QxPost(ContentTypeRelated, QxStarMixin):
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

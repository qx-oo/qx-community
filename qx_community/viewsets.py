from rest_framework import viewsets, decorators
from rest_framework.permissions import (
    IsAuthenticated, BasePermission, AllowAny
)
from django_filters import rest_framework as filters
from qx_base.qx_rest import mixins
from .serializers import (
    Comment,
    CommentSerializer,
    Star,
    StarSerializer,
)


class StarViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,):
    """
    点赞
    ---
    create:
        添加点赞

        添加点赞

    destory:
        取消点赞

        取消点赞
    """
    permission_classes = (
        IsAuthenticated,
    )
    queryset = Star.objects.all()
    serializer_class = StarSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class CommentFilter(filters.FilterSet):

    is_top = filters.BooleanFilter(
        field_name="parent", lookup_expr='isnull',
        help_text='是否父级评论, 1(父级), 0(子级), 不传为全部')
    type = filters.ChoiceField(
        choices=list(Comment.type_map_model.keys()), help_text="类型")

    class Meta:
        model = Comment
        fields = ('object_id', 'type', 'parent', 'is_top')


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return AllowAny().has_permission(request, view)
        return IsAuthenticated().has_permission(request, view)


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,):
    """
    评论
    ---
    list:
        评论列表

        评论列表

    retrieve:
        评论详情

        评论详情

    create:
        发布评论

        发布评论
    """
    permission_classes = (
        CommentPermission,
    )
    queryset = Comment.objects.all()

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            queryset = queryset.select_related(
                'user__userinfo', 'to_user__userinfo')
        return queryset

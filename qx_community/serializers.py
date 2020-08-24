from django.utils import timezone
from rest_framework import serializers
from .settings import community_settings


Comment = community_settings.COMMENT_MODEL
Star = community_settings.STAR_MODEL
Post = community_settings.POST_MODEL
UserSerializer = community_settings.COMMENT_USER_SERIALIZER_CLASS

comment_type = list(Comment.type_map_model.keys()) if Comment else []

star_type = list(Star.type_map_model.keys()) if Star else []


class StarSerializer(serializers.ModelSerializer):

    type = serializers.ChoiceField(
        star_type, label="类型:{}".format(star_type))

    class Meta:
        model = Star
        fields = ('id', 'object_id', 'type', 'created')
        read_only_fields = ('id', 'created')


class CreateCommentSerializer(serializers.ModelSerializer):

    type = serializers.ChoiceField(
        comment_type, label="类型:".format(comment_type))

    def create(self, validated_data):
        user = self.context['request'].user

        forbiden_time = timezone.now() + timezone.timedelta(seconds=5)
        if Comment.objects.filter(
                user=user, created__gt=forbiden_time).exists():
            raise serializers.ValidationError('您的评论频率过高,请稍后重试')

        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = (
            'id', 'object_id', 'type', 'user', 'to_user', 'content', 'parent',
            'created', 'star',)
        read_only_fields = ('id', 'user', 'created', 'star',)


class ChildCommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(
        label="评论用户")
    to_user = UserSerializer(
        label="被回复用户")
    type = serializers.ChoiceField(
        comment_type, label="类型:".format(comment_type))

    class Meta:
        model = Comment
        fields = (
            'id', 'object_id', 'type', 'user', 'to_user', 'content', 'parent',
            'created', 'star',)


class CommentSerializer(ChildCommentSerializer):

    comment_set = ChildCommentSerializer(
        label="二级评论", many=True)

    class Meta:
        model = Comment
        fields = ChildCommentSerializer.Meta.fields + (
            'comment_set',)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'created', 'info'
        )

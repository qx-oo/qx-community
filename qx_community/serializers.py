from rest_framework import serializers
from .settings import community_settings


Comment = community_settings.COMMENT_MODEL
Star = community_settings.STAR_MODEL
Post = community_settings.POST_MODEL
UserSerializer = community_settings.COMMENT_USER_SERIALIZER_CLASS

comment_type = []
if Comment:
    comment_type = list(Comment.type_map_model.keys())

star_type = []
if Star:
    star_type = list(Star.type_map_model.keys())


class StarSerializer(serializers.ModelSerializer):

    type = serializers.ChoiceField(
        star_type, label="类型:".format(star_type))

    class Meta:
        model = Star
        fields = ('id', 'object_id', 'type', 'created')
        read_only_fields = ('id', 'created')


class CreateCommentSerializer(serializers.ModelSerializer):

    type = serializers.ChoiceField(
        comment_type, label="类型:".format(comment_type))

    def create(self, validated_data):
        # TODO: 添加频繁发布限制
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = (
            'id', 'object_id', 'type', 'user', 'to_user', 'content', 'parent',
            'created')
        read_only_fields = ('id', 'user', 'created')


class CommentSerializer(CreateCommentSerializer):

    user = UserSerializer()
    to_user = UserSerializer()


class


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'created', 'info'
        )

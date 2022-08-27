from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'

    def create(self, validated_data):
        if validated_data['user'] == validated_data['following']:
            raise serializers.ValidationError(
                'Пользователь не может подписаться сам на себя'
            )

        follow, created = self.Meta.model.objects.get_or_create(
            **validated_data
        )

        if not created:
            raise serializers.ValidationError("Уже подписан")

        return follow

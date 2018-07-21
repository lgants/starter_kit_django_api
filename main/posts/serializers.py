from rest_framework import serializers
from .models import (Post, Comment)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content')


class PostSerializer(serializers.ModelSerializer):
    # title = serializers.CharField()
    # content = serializers.CharField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content')

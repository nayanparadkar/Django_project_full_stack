from rest_framework import serializers
from ..models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Tweet
        fields = ["id", "user", "content", "photo", "created_at", "updated_at"]

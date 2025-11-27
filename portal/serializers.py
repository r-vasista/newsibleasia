# portal/serializers.py
from rest_framework import serializers
from post_management.models import NewsPost, Tag

class NewsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPost
        fields = "__all__"

    def _extract_tags(self, post_tag_str):
        # Split by comma instead of whitespace
        tags = [tag.strip().lstrip("#") for tag in post_tag_str.split(",") if tag.strip()]
        return tags

    def create(self, validated_data):
        post_tag_str = validated_data.get("post_tag", "")
        news_post = super().create(validated_data)

        if post_tag_str:
            for tag_name in self._extract_tags(post_tag_str):
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                news_post.tags.add(tag)
        return news_post

    def update(self, instance, validated_data):
        post_tag_str = validated_data.get("post_tag", "")
        news_post = super().update(instance, validated_data)

        if post_tag_str:
            news_post.tags.clear()
            for tag_name in self._extract_tags(post_tag_str):
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                news_post.tags.add(tag)
        return news_post


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']
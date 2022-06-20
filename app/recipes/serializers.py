"""
Serializers for recipe APIs.
"""

from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        # list all fields that we want to use with the serializer:
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']  # because we don't want to change id

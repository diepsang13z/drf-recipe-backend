"""
Serializers for Recipe APIs.
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient object."""

    class Meta():
        model = Ingredient
        fields = [
            'id',
            'name',
        ]
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe objects."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'time_minutes',
            'price',
            'link',
            'tags',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', [])
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    # Private
    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, _ = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            recipe.tags.add(tag_obj)


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for Recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

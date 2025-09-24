from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.profile.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    # ingebouwde rest_framework validatiesysteem.
    # wordt aangeroepen iedere keer dat er een post aangemaakt
    # of bijgewerkt wordt
    def validate_image(self, value):
        # 1024 kilobytes, vermenigvuldigd met 1024 --> megabytes,
        # vermenigvuldigd met 2 ---> 2 MB
        # Indien de ingeladen afbeelding groter dan 2 MB is,
        # dan gaan we een foutmelding retourneren
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        # regel voor validatie hoogte (4096 pixels)
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidatieError(
                'Image width larger than 4096px!'
            )
        # Na al deze validaties moeten we uiteraard de "value" retourneren
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # Als we een post oplijsten of ophalen, zien we een like_id veld
    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            # als de ingelogde user de post (post=obj) heeft geliked,
            # dan zal like.id geretourneerd worden, anders None
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'image_filter',
            'like_id', 'comments_count', 'likes_count',
        ]

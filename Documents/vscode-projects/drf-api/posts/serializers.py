from rest_framework import serializers
from .models import Posts


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.profile.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyFiled(source="owner.profile.image.url")

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
        return value

    def get_is_owner(self, obj):
        request = self.content['request']
        return request.user == obj.owner

    class Meta:
        model = Posts
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'image_filter',
        ]

from rest_framework import serializers
from .models import Posts


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.profile.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyFiled(source="owner.profile.image.url")

    def get_is_owner(self, obj):
        request = self.content['request']
        return request.user == obj.owner

    class Meta:
        model = Posts
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image'
        ]

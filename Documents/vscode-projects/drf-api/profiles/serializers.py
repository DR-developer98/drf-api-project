from rest_framework import serializers
from .models import Profile


# de naam van deze klasse moet intuïtief terug te voeren zijn 
# tot het Profile model ===> ModelSerializer ===> ProfileSerializer(serializers.ModelSerializer)
class ProfileSerializer(serializers.ModelSerializer):
    # Dit is, opdat dit veld niet bijgewerkt kan worden
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Profile
        # Hier specificeer ik de velden van het model, die ik
        # in de respon geretourneerd wil zien.
        # Let op: wanneer je een model door extensie van het .model
        # creëert (d.w.z. models.Model), dan wordt de primary key "id" automatisch 
        # aangemaakt.
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image'
        ]
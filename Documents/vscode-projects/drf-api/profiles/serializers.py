from rest_framework import serializers
from .models import Profile
from followers.models import Follower


# de naam van deze klasse moet intuïtief terug te voeren zijn
# tot het Profile model ===> ModelSerializer ===>
# ProfileSerializer(serializers.ModelSerializer)
class ProfileSerializer(serializers.ModelSerializer):
    # Dit is, opdat dit veld niet bijgewerkt kan worden
    owner = serializers.ReadOnlyField(source="owner.username")
    # Door .SerializerMethodField te gebruiken,
    # zorgen we voor de "Read-only"-heid van dit veld,
    # d.w.z. dat het niet aangepast kan worden
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    # om de waarde van "is_owner" op te halen,
    # gebruiken we de volgende methode
    def get_is_owner(self, obj):
        # we krijgen nu toegang tot het context-object
        # zoals hieronder getoond
        request = self.context['request']
        # onderstaand retourneert true, indien de gebruiker
        # die de request maakt ook de eigenaar van het object is
        return request.user == obj.owner
        # ↓↓↓ daarna voegen we 'is_owner' toe aan de field-array ↓↓↓

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            # indien de ingelogde user de eigenaar van dit profield volgt
            # zal er dan een following.id geretourneerd worden
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            # print(following)
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        # Hier specificeer ik de velden van het model, die ik
        # in de respon geretourneerd wil zien.
        # Let op: wanneer je een model door extensie van het .model
        # creëert (d.w.z. models.Model), dan wordt de primary key "id"
        # automatisch aangemaakt. 
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
        ]

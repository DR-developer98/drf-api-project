from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class ProfileList(APIView):
    """
    List all profiles
    No Create view (post method), as profile creation handled by django signals
    """
    # Dit is de get-methode
    def get(self, request):
        # Hiermee retourneren we alle profielen
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        # We retourneren alle profielen in de respons
        return Response(serializer.data)

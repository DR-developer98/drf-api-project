from rest_framework import generics, permissions
from DRF_API.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer

# generics. (= generic view) .List(=verzorgt GET) Create(=verzorgt PUT)
class CommentList(generics.ListCreateAPIView):
    """
    List comments or create a comment if logged in.
    """
    # Dit zorgt voor een mooi invulformulier
    serializer_class = CommentSerializer
    # Voorkomt dat anonieme gebruikers opmerkingen plaatsen
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # we willen hier alle instanties van de Comments onder een post
    queryset = Comment.objects.all()

    # Dit zorgt ervoor dat comments automatisch gekoppeld worden 
    # aan de gebruiker die ze plaats, op het moment dat
    # de gebruiker wordt aangemaakt.
    # Dus: gebruiker is aangemaakt => alle opmerkingen die hij zal achterlaten
    # zullen met hem geassocieerd worden
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serialier_class = CommentDetailSerializer
    queryset = Comment.objects.all()

from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from DRF_API.permissions import IsOwnerOrReadOnly

class PostList(APIView):
    """
    List all posts
    No Create view (post method)
    """
    # serializer_class = PostSerializer --->
    # zorgt voor een mooi invulformulier voor de
    # aanmaak van posts
    serializer_class = PostSerializer
    # bovenaan hebben we "permissions" geïmporteerd
    # hiermee zorgen ervoor, dat alleen een ingelogde
    # gebruiker een nieuwe post aan kan maken
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    # get methode
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
            )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            # indien de serializer akkoord is,
            # zal 201 als status geretourneerd worden
            # succesvolle creatie
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        # indien serializer niet akkoord is,
        # dan zal 400 als status geretourneerd worden
        # bad request (gegevens niet begrepen door API of gewoon foutief)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    

class PostDetail(APIView):
    """
    Returns one single post based on its id
    Handles inexistance of a post
    Updates one single post based on its id
    Delete one single post based on its id
    """
    serializer_class = PostSerializer
    # Alleen een ingelogde gebruiker kan een post
    # editen of deleten
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        # Het is hier niet nodig om many=True door te geven aan de Serializer
        # Dit is, omdat we met één enkele instantie van een profiel te maken 
        # hebben
        serializer = PostSerializer(
            post, context={'request': request}
            )
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data,
            context={'request': request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
                status=status.HTTP_204_NO_CONTENT
            )

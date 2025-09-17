from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    """
    List all posts
    No Create view (post method)
    """
    # serializer_class = PostSerializer --->
    # zorgt voor een mooi invulformulier voor de
    # aanmaak van posts
    serializer_class = PostSerializer
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
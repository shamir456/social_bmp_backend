from social_bmp_backend.api.models import Posts
from rest_framework import viewsets
from social_bmp_backend.api.serializers import PostsSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.response import Response


class PostsCreateSet(generics.CreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        if isinstance(data, list):  # <- is the main logic
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostsViewSet(generics.ListAPIView):
        serializer_class= PostsSerializer
        queryset = Posts.objects.all()



    # def get(self, request, format=None):
    #     posts = Posts.objects.all()
    #     serializer = PostsSerializer(posts, many=True)
    #     return Response(serializer.data, safe=False)


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
# # Create your views here.

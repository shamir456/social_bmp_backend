from social_bmp_backend.api.models import Posts
from rest_framework import viewsets
from social_bmp_backend.api.serializers import PostsSerializer,PostSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from langdetect import detect
from rest_meets_djongo import serializers
from rest_framework import mixins
from django.views.generic import DetailView,ListView,CreateView, UpdateView, DeleteView


from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.decorators import api_view
from rest_framework.response import Response
import pymongo


from rest_framework.pagination import PageNumberPagination

class StandardResultsPagination(PageNumberPagination):
	page_size=50
	page_size_query_param='page_size'
	max_page_size=1000

class PostListView(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = PostsSerializer
    queryset = Posts.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]



    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def put(self, request, id=None):
        return self.update(request, id)

    def perform_update(self, serializer):
        print(self.request.user)
        serializer.save(created_by=self.request.user)        

    def delete(self, request, id=None):
        return self.destroy(request, id)

	

class PostsCreateSet(generics.CreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    lookup_field = 'id'

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

    def put(self,request,id=None):
    	data = request.data
    	instance = Posts.objects.get(pk=id)
    	serializer = PostsSerializer(instance, data=data)
    	if serializer.is_valid():
    		serializer.save()
    		return Response(serializer.data, status=200)
    	return Response(serializer.erros, status=400)

class PostsViewSet(generics.ListAPIView):
        serializer_class= PostSerializer
        queryset = Posts.objects.all().order_by('id')
        pagination_class=StandardResultsPagination
        

        # def get(self, request, format=None):
        # 	posts = Posts.objects.all()
        # 	serializer = PostsSerializer(posts, many=True)
        # 	 # if serializer.is_valid():
        # 	# 	print(serializer.data)
        # 	# 	for post in serializer.data:
	       #  # 		print(post)
	       #  # 		for comment in post['comments']:
	       #  # 			try:
	       #  # 				lang = detect(comment['comment_message'])
	       #  # 			except:
	       #  # 				lang=''
	        				

	       #  # 			if(lang == 'ur'):
	       #  # 				print('message is in urdu')
	       #  # 				comment['lang_type']='ur'
	       #  # 			elif(lang== 'en'):
	       #  # 				print('message is in english')
	       #  # 				comment['lang_type']='en'
	       #  # 			elif(lang==''):
	       #  # 				comment['lang_type']=''
	       #  # 			else:
	       #  # 				print('message is in roman urdu')
	       #  # 				comment['lang_type']='roman'
        # 	# 	print(serializer.data)
        # 	# 	serializer.save()
        # 	return Response(serializer.data, status=status.HTTP_200_OK)

        	# print(posts[2:5])

        	
        	




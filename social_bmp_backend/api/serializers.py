from rest_framework import serializers
from social_bmp_backend.api.models import Posts
from djongo import models
from rest_meets_djongo import serializers
class PostsSerializer(serializers.DjongoModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     many = kwargs.pop('many', True)
    #     super(PostsSerializer, self).__init__(many=many, *args, **kwargs)


    class Meta:
        model = Posts
        fields = ['post_id','page_id','post_type','comments','post_published']



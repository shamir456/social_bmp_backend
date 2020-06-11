from rest_framework import serializers
from social_bmp_backend.api.models import Posts
from djongo import models
from rest_meets_djongo import serializers
class PostsSerializer(serializers.DjongoModelSerializer):

    class Meta:
        model = Posts
        fields = ['post_id','page_id','post_message','post_type','post_published','All','num_shares','num_comments','Like','Wow','Love','Haha','Sad','Angry','comments']




class PostSerializer(serializers.DjongoModelSerializer):

	class Meta:
		model=Posts
		fields=['id','post_id','page_id','post_type','post_published','All','num_shares','num_comments','Like','Wow','Love','Haha','Sad','Angry']


from djongo import models
from django import forms

# Create your models here.

class Comments(models.Model):
	comment_id=models.CharField(max_length=20)
	comment_message=models.TextField(blank=True)
	comment_author=models.TextField()
	comment_time =models.TextField(blank=True)
	scraped_time=models.DateTimeField(max_length=20)
	lang_type=models.CharField(max_length=20,blank=True)
	sentiment=models.CharField(max_length=10,blank=True)

	class Meta:
		abstract = True 


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = (
            'comment_id', 'comment_message','comment_time','lang_type','comment_author','scraped_time','sentiment'
        )
		

class Posts(models.Model):
	post_id=models.CharField(max_length=20,unique=True)
	post_message=models.TextField(blank=True)

	page_id=models.CharField(max_length=20)
	post_type=models.CharField(max_length=10)
	post_published=models.DateTimeField(max_length=20)
	num_shares=models.CharField(max_length=10)  
	num_comments=models.CharField(max_length=10)  
	All = models.CharField(max_length=10,blank=True)
	Like = models.CharField(max_length=10,blank=True) 
	Wow = models.CharField(max_length=10,blank=True) 
	Love = models.CharField(max_length=10,blank=True) 
	Haha = models.CharField(max_length=10,blank=True) 
	Sad = models.CharField(max_length=10,blank=True)
	sentiment=models.CharField(max_length=10,blank=True)
	Angry = models.CharField(max_length=10,blank=True) 
	# objects = models.DjongoManager()
	comments=models.ArrayModelField(
		model_container=Comments,
		model_form_class=CommentsForm
		)
	objects = models.DjongoManager()

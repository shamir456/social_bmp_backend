from djongo import models
from django import forms

# Create your models here.

class Comments(models.Model):
	comment_id=models.CharField(max_length=20)
	comment_message=models.TextField()
	class Meta:
		abstract = True 


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = (
            'comment_id', 'comment_message'
        )
		

class Posts(models.Model):
	post_id=models.CharField(max_length=20)
	page_id=models.CharField(max_length=20)
	post_type=models.CharField(max_length=10)
	post_published=models.DateTimeField(max_length=14)
	post_message=models.TextField()
	#objects = models.DjongoManager()
	comments=models.ArrayModelField(
		model_container=Comments,
		model_form_class=CommentsForm
		)
	

objects = models.DjongoManager()

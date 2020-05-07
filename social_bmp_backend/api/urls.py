from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

from social_bmp_backend.api import views



urlpatterns = [
    path('posts/', views.PostsViewSet.as_view(),name='posts-api'),
    url(r'^add/', views.PostsCreateSet.as_view(), name='post-list'),
    path('post/<int:id>/', views.PostListView.as_view()),
    path('comments/authors/',views.AuthorViewSet.as_view(),name='author-list'),
    path('comments/sentiment/',views.SentimentViewSet.as_view(),name='sentiment-list'),
    path('posts/count/',views.DataViewSet.as_view(),name='post-count'),
    path('comments/lang/',views.LanguageViewSet.as_view(),name='lang-count'),
    path('comments/lang_sentiment/',views.Language_SentimentViewSet.as_view(),name=''),
    path('comments/language-time/',views.Language_TimeViewSet.as_view(),name=''), #comments languages w.r.t to time are sent using this endpoint
    path('comments/sentiment-time/',views.Sentiment_TimeViewSet.as_view(),name=''), #comments sentiment w.r.t time are sent using this endpoint
    path('posts/reacts',views.Post_ReactViewSet.as_view(),name='post-reacts'), #post reacts are sent using this endpoint
    path('posts/types',views.Post_TypeViewSet.as_view(),name='post-types') ,#post types are sent using this endpoint
    path('posts/user-profile/',views.UserProfileViewSet.as_view(),name='post-profile'),
    path('top-comments',views.TopComment.as_view(),name='top-comments')



]

urlpatterns = format_suffix_patterns(urlpatterns)

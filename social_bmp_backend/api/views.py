from social_bmp_backend.api.models import Posts
from rest_framework import viewsets
from social_bmp_backend.api.serializers import PostsSerializer, PostSerializer
from bson.son import SON
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from langdetect import detect
from rest_meets_djongo import serializers
from rest_framework import mixins
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView


from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.decorators import api_view
from rest_framework.response import Response
import pymongo


from rest_framework.pagination import PageNumberPagination


from textblob import TextBlob
import json
import time
import re
import fasttext
import joblib


class StandardResultsPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostListView(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = PostsSerializer
    queryset = Posts.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsAdminUser]
    # pagination=StandardResultsPagination

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
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def __init__(self):

        self.PRETRAINED_MODEL_PATH = '/home/zen/lid.176.bin'
        self.model = fasttext.load_model(self.PRETRAINED_MODEL_PATH)
        self.roman_model=joblib.load('/home/zen/roman-urdu.pkl')
        

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = PostsSerializer(queryset, many=True)
    #     return Response(serializer.data)
    def process_text(self, input_review):
    #     input_review = input_review.astype(str).str.lower() #converting to lower case
    #     print(input_review)
    #     input_review = input_review.astype(str).str.replace('[{}]'.format(string.punctuation), '') #remove punctuation
    #     print(input_review)

    #     input_review = input_review.astype(strromanroman).str.replace("[^a-zA-Z#]",' ') #remove special characters
    #     print(input_review)

        input_review = re.sub(
            r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', input_review)
    #     print(input_review)
        input_review = input_review.lower()
       # print(input_review)
        return input_review
    def lemmatize_with_postag(self,sentence):
        sent = TextBlob(sentence)
        tag_dict = {"J": 'a', 
                    "N": 'n', 
                    "V": 'v', 
                    "R": 'r'}
        words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
        lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
        return " ".join(lemmatized_list)

    def convertAllFields(self,fields,data):
        for j in range(0,len(data)):
            for i in fields:
    #             print(data[j][i])
                data[j][i]=str(data[j][i])
                if (('k' in  data[j][i]) | ('K' in data[j][i])):
                    data[j][i]=data[j][i].replace('K','')
                    data[j][i]=data[j][i].replace('k','')
                    data[j][i]=str(int(float(data[j][i])*1000))
        return data

    def process_post_data_list(self,post_data):
        # PRETRAINED_MODEL_PATH = '/home/zen/lid.176.bin'
        # model = fasttext.load_model(PRETRAINED_MODEL_PATH)
        fields=['num_shares','num_comments','All','Like','Wow','Love','Haha','Sad','Angry']
        print("Data Loading...")
        data=self.convertAllFields(fields,post_data)
        print('Conversion....')
        for posts in data:
            i=0
            

            for comments in posts['comments']:
                lang_type=''
                comments['sentiment']=''
                comments['lang_type']=''

                comments['comment_message']=self.process_text(str(comments['comment_message']))
                if (("graphical emoji" == str(comments['comment_message'])) or ("Graphical Emoji"==str(comments['comment_message']))):
                    # print(comments)

                    print('here')
        #             posts['comments'].remove(comments)
                    comments['lang_type']=''
                    comments['comment_message']=''
        #             print(comments['comment_message'])
                    del posts['comments'][i]
                    i=i+1
                    
                else:
                    comments['comment_message']=comments['comment_message'].replace('\n','')
                    analysis=TextBlob('u'+comments['comment_message'])
                    comment_message=comments['comment_message']
                    i=i+1

                    lang_type=self.model.predict(str(comment_message))            
                    if lang_type[0][0] == '__label__en' and lang_type[1][0] > 0.7:
                            comments['lang_type']='english_lang'
                            print('english')
                    elif lang_type[0][0] == '__label__ur' and lang_type[1][0] > 0.7:
                        comments['lang_type']='urdu_lang'
                        print('urdu')
                    else:
                        comments['lang_type']='roman'

        for posts in data:
            
            for comments in posts['comments']:
                # print(comments['comment_message'],comments['lang_type'])

                # comments['sentiment']=''
                if comments['lang_type'] == 'roman':
                    comments['sentiment']=str(self.roman_model.predict([comments['comment_message']])[0])
                    
            
                if comments['lang_type'] == "english_lang":
                    message=self.lemmatize_with_postag(comments['comment_message'])
                    analysis=TextBlob(message)
                    # print(analysis.sentiment.polarity)

                    i=i+1
                    if analysis.sentiment.polarity < -0.1:
                        comments['sentiment']='Negative'
                    elif analysis.sentiment.polarity >= 0.5:
                        comments['sentiment']='Positive'
                    else:
                        comments['sentiment']='Neutral'        

        return data




    def post(self, request, format=None):
        data = request.data
        if isinstance(data, list):  # <- is the main logic
            processed_data=self.process_post_data_list(data)
            # complete_data=self.perform_sentiment()
            serializer = self.get_serializer(data=data, many=True)

        else:
            serializer = self.get_serializer(data=data)


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
        queryset = Posts.objects.all()
        authentication_classes = [TokenAuthentication,]
        permission_classes = [IsAuthenticated]
        # print(queryset)
        # pagination_class=StandardResultsPagination
        

        # def get(self, request, format=None):
        #     posts = Posts.objects.all()
        #     serializer = PostSerializer(posts, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)

            # print(posts[2:5])

pipline=[
  {
    "$unwind": "$comments"
  },
  {
    "$group": {
      "_id": "$comments.comment_author",
      "count": {
        "$sum": 1
      },
      "posts": {
        "$push": {
          "$concat": [
            "$page_id",
            "/posts/",
            "$post_id"
          ]
        }
      }
    }
  },
  {
    "$sort": {
      "count": -1
    }
  },
  {
    "$limit": 50
  }
]
class AuthorViewSet(generics.ListAPIView):


    def get(self,request):
        author=Posts.objects.mongo_aggregate(pipline)
        print(author)
        return Response(author,status=status.HTTP_200_OK)


sentiment_pipeline=[ {"$unwind":"$comments"},  
{ "$group":{ "_id":"$comments.sentiment", "count":{"$sum":1}  } } 

]

post_pipeline=[ { "$group": {     "_id": {"year":{"$year":"$post_published"},"month":{"$month":"$post_published"}
},     "count": { "$sum": 1} ,"time_year":{"$first":"$post_published"}}},{ "$sort": { "_id": -1 } } ]

class SentimentViewSet(generics.ListAPIView):
    queryset=Posts.objects.mongo_aggregate(pipline)

    def get(self,request):
        sentiment=Posts.objects.mongo_aggregate(sentiment_pipeline)
        print(sentiment)



        return Response(sentiment,status=status.HTTP_200_OK)

language_pipeline=[ {"$unwind":"$comments"},  
{ "$group":{ "_id":"$comments.lang_type", "count":{"$sum":1}  } } 

]


class LanguageViewSet(generics.ListAPIView):
    def get(self,request):
        language=Posts.objects.mongo_aggregate(language_pipeline)
        return Response(language,status=status.HTTP_200_OK)

class DataViewSet(generics.ListAPIView):

    def get(self,request):
        user_profiles=Posts.objects.mongo_aggregate(post_pipeline)

        return Response(user_profiles,status=status.HTTP_200_OK)


language_sentiment_pipeline=[
  {
    "$unwind": "$comments"
  },
  {
    "$group": {
      "_id": {
        "year": {
          "$year": {
            "$toDate": "$post_published"
          }
        },
        "month": {
          "$month": {
            "$toDate": "$post_published"
          }
        },
        "post_sentiment": "$comments.sentiment",
        "comment_lang": "$comments.lang_type"
      },
      "count": {
        "$sum": 1
      }
    }
  },
  {
    "$sort": {
      "_id": -1
    }
  }
]


class Language_SentimentViewSet(generics.ListAPIView):
    def get(self,request):
        language_sentiment=Posts.objects.mongo_aggregate(language_sentiment_pipeline)
        return Response(language_sentiment,status=status.HTTP_200_OK)


language_time_pipeline=[
  {
    "$unwind": "$comments"
  },
  {
    "$group": {
      "_id": {
        "year": {
          "$year": {
            "$toDate": "$post_published"
          }
        },
        "month": {
          "$month": {
            "$toDate": "$post_published"
          }
        }
        # ,
        # "week": { "$week": { "$toDate": "$post_published" } }

        ,
        "comment_lang": "$comments.lang_type"
      },
      "count": {
        "$sum": 1
      }
    }
  },
  {
    "$sort": {
      "_id": -1
    }
  }
]

class Language_TimeViewSet(generics.ListAPIView):
    def get(self,request):
        language_time=Posts.objects.mongo_aggregate(language_time_pipeline)
        return Response(language_time,status=status.HTTP_200_OK)


sentiment_time_pipeline=[
  {
    "$unwind": "$comments"
  },
  {
    "$group": {
      "_id": {
        "year": {
          "$year": {
            "$toDate": "$post_published"
          }
        },
        "month": {
          "$month": {
            "$toDate": "$post_published"
          }
        }
        # ,
        # "week": { "$week": { "$toDate": "$post_published" } }

        ,
        "post_sentiment": "$comments.sentiment",
      },
      "count": {
        "$sum": 1
      }
    }
  },
  {
    "$sort": {
      "_id": -1
    }
  }
]

class Sentiment_TimeViewSet(generics.ListAPIView):
    def get(self,request):
        sentiment_time=Posts.objects.mongo_aggregate(sentiment_time_pipeline)
        return Response(sentiment_time,status=status.HTTP_200_OK)

post_reacts_pipeline=[
  {
    "$group": {
      "_id": {
        
        "year": {
          "$year": { "$toDate": "$post_published" }
        },
        "month": {
          "$month": { "$toDate": "$post_published" }
        }
      },
      "angry": {
        "$sum": {
          "$toInt": "$Angry"
        }
      },"haha": {
        "$sum": {
          "$toInt": "$Haha"
        }
      },"wow": {
        "$sum": {
          "$toInt": "$Wow"
        }
      },"sad": {
        "$sum": {
          "$toInt": "$Sad"
        }
      },"all": {
        "$sum": {
          "$toInt": "$All"
        }
      },"like": {
        "$sum": {
          "$toInt": "$Like"
        }
      },
      "post_count": {
        "$sum": 1
      }
    }
    
  },
  { "$sort": { "_id": -1 } }
]


class Post_ReactViewSet(generics.ListAPIView):
    def get(self,request):
        post_reacts=Posts.objects.mongo_aggregate(post_reacts_pipeline)
        return Response(post_reacts,status=status.HTTP_200_OK)

post_type_pipeline=[
{
    "$group": {
      "_id": {
        "year": {
          "$year": {
            "$toDate": "$post_published"
          }
        },
        "month": {
          "$month": {
            "$toDate": "$post_published"
          }
        },

        "post_type":"$post_type"
      },
      "count": {
        "$sum": 1
      }
    }
  },
  {
    "$sort": {
      "_id": -1
    }
  }
]



class Post_TypeViewSet(generics.ListAPIView):
    def get(self,request):
        post_types=Posts.objects.mongo_aggregate(post_type_pipeline)
        return Response(post_types,status=status.HTTP_200_OK)








user_profiling= [
    {
        "$unwind": "$comments"
    },
    { "$match" : { "comments.comment_author" : "" } },
    {
        "$group": {
            "_id": "$comments.comment_author",
            "count": {
                "$sum": 1
            },
            "comments": {
                "$push": {
                    "comment_sentiment": "$comments.sentiment","comment_id": "$comments.comment_id","comment_message": "$comments.comment_message","comment_author":"$comments.comment_author","post_message":"$post_message", "post_time": "$post_published", "post_id": {
                        "$concat": [
                            "facebook.com/", "$page_id",
                            "/posts/",
                            "$post_id"
                        ]
                    }
                }
            }
        }
    },
    {
        "$sort": {
            "count": -1
        }
    }
    ,
    {
        "$limit": 50
    }
]


class UserProfileViewSet(generics.ListAPIView):
    queryset=Posts.objects.mongo_aggregate(user_profiling)
    pagination_class=StandardResultsPagination

    def get(self,request,*args,**kwargs):
        query=request.GET.get("q")
        print(query)
        user_profiling[1]['$match']['comments.comment_author']=query
        print(user_profiling[1]['$match']['comments.comment_author'])
        user_profiles=Posts.objects.mongo_aggregate(user_profiling)
        return Response(user_profiles,status=status.HTTP_200_OK)


top_comments=[
    {
        "$unwind": "$comments"
    },
    {
        "$group": {
            "_id": "$post_published",
            "count": {
                "$sum": 1
            },
            "comments": {
                "$push": {
                    "comment_sentiment": "$comments.sentiment","comment_author": "$comments.comment_author","comment_message": "$comments.comment_message", "post_time": "$post_published", "post_id": {
                        "$concat": [
                            "https://facebook.com/", "$page_id",
                            "/posts/",
                            "$post_id",
                            '/?comment_id=',
                            '$comments.comment_id',

                        ]
                    }
                }
            }
        }
    },
    {
        "$sort": {
            "_id": -1
        }
    },
    {
        "$limit": 10
    }
]


class TopComment(generics.ListAPIView):

    def get(self,request):
        top_comment=Posts.objects.mongo_aggregate(top_comments)
        return Response(top_comment,status=status.HTTP_200_OK)
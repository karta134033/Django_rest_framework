from rest_framework import serializers
from .models import Article
from django.contrib.auth.models import User, Group

# class ArticleSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     author = serializers.CharField(max_length=100)
#     email = serializers.EmailField(max_length=100)
#     data = serializers.DateTimeField()
#     def create(self, validated_date):
#         return Article.objects.create(validated_date)
#     def update(self, instance, validated_date):
#         instance.title = validated_date.get('title', instance.title)
#         instance.author = validated_date.get('author', instance.author)
#         instance.email = validated_date.get('title', instance.email)
#         instance.date  = validated_date.get('title', instance.date)
#         instance.save()
#         return instance


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'email', 'date']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

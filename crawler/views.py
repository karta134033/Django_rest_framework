import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class CsvViewSet(viewsets.ViewSet):  # viewsets.ViewSet 需要將以下function寫出
                                     # viewsets 需要以register的方式註冊
    def list(self, request):
        return

    def create(self, request):  # put
        result_string = ""
        data = request.data
        query = data.pop('file')
        print(query)
        print(query[0].open())
        filename = 'csv_file/' + str(query[0].open())
        try:
            os.remove(filename)
        except:
            print(filename + '未建立')
        print(filename)
        data = query[0].read()
        path = default_storage.save(filename, ContentFile(data))
        return Response(result_string)

    def retrieve(self, request, pk=None):
        return

    def update(self, request, pk=None):
        return

#---------------------------版本5-------------------------#

class ArticleGenericViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def post(self, request):
        return self.create(request)

    def post(self, request):
        return self.create(request)

    def delete(self, request, id):
        return self.destroy(request, id)

#---------------------------版本4-------------------------#

class ArticleViewSet(viewsets.ViewSet):  # viewsets.ViewSet 需要將以下function寫出
                                         # viewsets 需要以register的方式註冊
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)  # 重點:many=true
        return Response(serializer.data)

    def create(self, request):  # put
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data)  # 指定更新某個article
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------------版本3-------------------------#

class GenericAPIView(
        generics.GenericAPIView, 
        mixins.ListModelMixin, 
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,  # 需有Retrieve才能綁定Update
        mixins.DestroyModelMixin):

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'  # 加此段才能正確put資訊
    # authentication_classes = [SessionAuthentication, BasicAuthentication]  # 先確定Session認證 若無則再確認Basic認證
    authentication_classes = [TokenAuthentication]  # 在/admin中新增  最後在postman->Header->KEY: Authorization value:TOKEN c08a5bb40ed8ac01d3ee5f86bb686a8a019178e9
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        # 不用在get post等方法中去調用Article.objects.all()
        if id: return self.retrieve(request)
        else: return self.list(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

#---------------------------版本2-------------------------#

class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)  # 重點:many=true
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)  # 因為只要單個，所以不用設定為many=true
        return Response(serializer.data)  # 也不用加save

    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)  # 指定更新某個article
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------版本1-------------------------#

@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)  # 重點:many=true 
        return Response(serializer.data)
    elif request.method =='POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    try: 
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)  # 因為只要單個，所以不用設定為many=true
        return Response(serializer.data)  # 也不用加save
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data) # 指定更新某個article
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

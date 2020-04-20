from django.urls import path, include
from .views import article_list, article_detail, ArticleAPIView, ArticleDetails, GenericAPIView, ArticleViewSet, ArticleGenericViewSet
from rest_framework.routers import DefaultRouter  # 給ArticleViewSet 註冊用

router = DefaultRouter()  # rest_framework 內的  之後需要註冊在urlpatterns內才能使用
router.register('articles', ArticleViewSet, basename='article')  # 後方不用再加斜線
router.register('generic/article', ArticleGenericViewSet, basename='generic_article')


urlpatterns = [
  path('viewset/', include([
      path('', include(router.urls)),  # 可視位置 /viewset/articles/
      # path('<int:pk>/', include(router.urls))  # 無此段還是找的到該id
  ])),
  # path('article/', article_list),
  path('article/', ArticleAPIView.as_view()),  # 因為是傳入class 所以要再加上as_view
  # path('detail/<int:pk>', article_detail),
  path('detail/<int:id>', ArticleDetails.as_view()),
  path('generic/article/', include([
    path('', GenericAPIView.as_view()),
    path('<int:id>/', GenericAPIView.as_view()),  # 若無此段會page not found
  ])),
]

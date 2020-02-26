from django.urls import path
from .views import article_list, article_detail, ArticleAPIView

urlpatterns = [
    # path('article/', article_list),
    path('article/', ArticleAPIView.as_view()),  # 因為是傳入class 所以要再加上as_view
    path('detail/<int:pk>', article_detail),
]

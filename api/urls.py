from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from crawler import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls, name='admin_page'),  # 註冊admin頁面 
    path('crawler/', include('crawler.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

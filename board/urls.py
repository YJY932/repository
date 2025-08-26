from django.urls import path, include
from . import views
from .views import *    # 현재 패키지(.)에서 views.py 파일을 가져와 모든 함수와 클래스를 import함

urlpatterns = [
    path('',board,name='board'),    #views.board를 썼더니 from .views import *를 안씀
    path('<int:pk>/',boardDetail,name='detail'),
    path('post/',boardPost,name='post'),
    path('edit/<int:pk>/',boardEdit,name='edit'),
    path('delete/<int:pk>/',boardDelete,name='delete'),
    path('',page_view,name='page_view'),
]

app_name='board'
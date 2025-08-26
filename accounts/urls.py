from django.urls import path, include
from . import views
from .views import *    # 현재 패키지(.)에서 views.py 파일을 가져와 모든 함수와 클래스를 import함

urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    # path('signup2/',views.signup2, name='signup2'),
    path('signup/',signup,name='signup'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    # path('',home,name='home'),
]
app_name='accounts'